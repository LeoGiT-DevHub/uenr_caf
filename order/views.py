from datetime import date
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import generic
from finance.models import OrderPayment

from order.models import Cart, Order
from .forms import CartForm, OrderForm

today_date = date.today()



class MakeOrderView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
  template_name = 'order_form.html'
  success_url = reverse_lazy('order_detail')
  form_class = OrderForm
  success_message = "Order added successfully"
  
  def user_cart_items(self):
    cart = Cart.objects.filter(user=self.request.user.pk, ordered=False)
    qty =[]
    prices = []
    prices_to_pay = []
    discounts = []
    cart_items_dict ={}
    
    for item in cart:
      qty.append(item.qty)
      prices.append(item.price*item.qty)
      prices_to_pay.append(item.get_amount_to_pay*item.qty)
      discounts.append(item.get_discount)
      
    cart_items_dict.update([('qty', sum(qty)), ('amount', sum(prices)),  ('amount_to_pay', sum(prices_to_pay)), ('discount', sum(discounts))])
    return cart_items_dict

   
  def get_context_data(self, **kwargs):
    context = super(MakeOrderView, self).get_context_data(**kwargs)
    context.update({
      'user_cart': Cart.objects.filter(user = self.request.user, ordered=False),
      'user_cart_items': self.user_cart_items(),
      'user_orders': Order.objects.filter(cart__user = self.request.user),
    })
    return context

  def post(self, request):
    form = OrderForm(request.POST)
    cus_name = form['customer_name'].value()
    cus_contact = form['customer_contact'].value()
    cus_email = form['customer_email'].value()
    delivery_address = form['delivery_address'].value()
    address_des = form['address_description'].value()
    due_date = form['due_date'].value()
    served = form['served'].value()
    
    user_cart = Cart.objects.filter(user=request.user, ordered=False)
    if user_cart:
      order = Order.objects.create(
        customer_name = cus_name,
        customer_contact = cus_contact,
        customer_email = cus_email,
        delivery_address = delivery_address,
        address_description = address_des,
        due_date = due_date,
        served = served,
        processed_by = request.user
      )
      order.cart.set(user_cart)
      for cart in user_cart:
        cart.ordered = True
        cart.save()
        
      payment_method = form['payment_method'].value()
      if payment_method:
        payment = OrderPayment.objects.create(paid_for = order, amount=Decimal(order.amount_to_paid()) , paid_with=payment_method, paid_by = order.customer_name, through=request.user)
        return redirect('order_invoice', order.pk)
      
      return redirect('order_invoice', order.pk)
    return redirect('new_order')
  

class OrderDetailView(LoginRequiredMixin, SuccessMessageMixin, generic.DetailView):
  template_name = 'invoice.html'
  model = Order
  context_object_name = 'order'
    
  def get_context_data(self, **kwargs):
    context = super(OrderDetailView, self).get_context_data(**kwargs)
    context.update({
      'user_cart': Cart.objects.filter(user = self.request.user, ordered=False),
      'user_orders': Order.objects.filter(cart__user = self.request.user),
    })
    return context
    

class UserOrdersView(LoginRequiredMixin, generic.ListView):
  template_name = 'orders.html'
  model = Order
  context_object_name = 'orders'

  def get_context_data(self, **kwargs):
    context = super(UserOrdersView, self).get_context_data(**kwargs)
    context.update({
      'user_cart': Cart.objects.filter(user = self.request.user.pk, ordered=False),
      'user_orders': Order.objects.filter(processed_by = self.request.user.pk),
      'unserved_orders': Order.objects.filter(processed_by = self.request.user.pk, served = False),
    })
    return context

 
class OrdersTableView(LoginRequiredMixin, SuccessMessageMixin, generic.ListView):
  template_name = 'orders_db.html'
  queryset = Order.objects.all()
  context_object_name = 'orders'
  
  def get_context_data(self, **kwargs):
    context = super(OrdersTableView, self).get_context_data(**kwargs)
    context.update({
      'just_ordered':Order.objects.filter(date__date=today_date),
    })
    return context

 
class UpdateOrderView(LoginRequiredMixin, generic.UpdateView):
  template_name = 'order_form.html'
  success_url = reverse_lazy('order_detail')
  form_class = OrderForm
  success_message = "Order Updated successfully"
 
  def post(self, request):
    form = OrderForm(request.POST)
    form.updated_by = request.user
    if form.is_valid():
      form.save()
      return redirect('menu_detail')
      
    return render(request, self.template_name, context={'form':form})
  

class DeleteOrderView(LoginRequiredMixin, generic.DeleteView):
  template_name = 'confirm_delete.html'
  success_url = reverse_lazy('orders')
  model = Order
  success_message = "Menu Deteled successfully"


class UserCartView(LoginRequiredMixin, generic.ListView):
  template_name = 'cart.html'
  queryset = Cart.objects.filter(ordered=False)
  context_object_name = 'cart'
  
  def user_cart_items(self):
    cart = self.queryset.filter(user=self.request.user.pk)
    qty =[]
    prices = []
    prices_to_pay = []
    cart_items_dict ={}
    
    for item in cart:
      qty.append(item.qty)
      prices.append(item.price*item.qty)
      prices_to_pay.append(item.get_amount_to_pay*item.qty)
      
    cart_items_dict.update([('qty', sum(qty)), ('amount', sum(prices)),  ('amount_to_pay', sum(prices_to_pay))])
    return cart_items_dict

  def get_context_data(self, **kwargs):
    context = super(UserCartView, self).get_context_data(**kwargs)
    context.update({
      'user_cart': Cart.objects.filter(user = self.request.user.pk, ordered=False),
      'user_cart_items': self.user_cart_items(),
      'user_orders': Order.objects.filter(processed_by = self.request.user.pk),
      'unserved_orders': Order.objects.filter(processed_by = self.request.user.pk, served = False),
    })
    return context

  def post(self, request, *args, **kwargs):
    if request.POST.get('delete'):
      cart = Cart.objects.get(pk=request.POST['delete'])
      messages.success(request, f"{cart.menu.name} Removed from Cart !")
      cart.delete()
      return redirect('user_cart')
    if request.POST.get('cart'):
      cart = Cart.objects.get(pk=request.POST['cart'])
      plus_minus = int(request.POST['plus_minus'])
      if cart.qty > 1:
        cart.qty += plus_minus
      elif plus_minus == 1:
        cart.qty += plus_minus    
      cart.save()
      messages.success(request, f"{cart.menu.name} Updated Successfully !")
      return redirect('user_cart')
 
