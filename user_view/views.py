from datetime import date
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from menu.models import Menu, MenuCategory
from order.models import Cart
from order.forms import CartForm

today_date = date.today()
class HomePageView(generic.ListView):
  template_name = 'index.html'
  queryset = Menu.objects.order_by('-updated_on')
  context_object_name = 'menu'
    
  def get_context_data(self, **kwargs):
    context = super(HomePageView, self).get_context_data(**kwargs)
    context.update({
      'category': MenuCategory.objects.all(),
      'just_added': Menu.objects.filter(date__date=today_date),
    })
    return context
  
  def post(self, *args, **kwargs):
    user = self.request.user
    try:
      menu = Menu.objects.get(pk=self.request.POST['menu'])
    except:
      menu = None
    try:
      buy_now = Menu.objects.get(pk=self.request.POST['buy_now'])
    except:
      buy_now = None
    try:
      cart = CartForm.objects.get(user=user, ordered=False, menu=menu or buy_now)
    except:
      cart = False
    if menu is not None and cart:
      cart.qty = cart.qty+1
      cart.save()
      messages.success(self.request, f"{cart.menu.name} Updated in Cart; Quantity is now {cart.qty}")
    elif menu is not None:
      price = menu.price
      discount = menu.get_discount()
      cart = Cart.objects.create(user=user, menu=menu, price=price, discount=discount)
      messages.success(self.request, f"{cart.menu.name} Added to Cart Successfully")
      
    elif buy_now and cart:
      cart.qty = cart.qty+1
      cart.save()
      messages.success(self.request, f"{cart.menu.name} Updated in Cart; Quantity is now {cart.qty}")
      return redirect('user_cart')
       
    elif buy_now:
      price = buy_now.price
      discount = buy_now.get_discount()
      cart = Cart.objects.create(user=user, menu=buy_now, price=price, discount=discount)
      messages.success(self.request, f"{cart.menu.name} Added to Cart Successfully")
      return redirect('user_cart')
       
      
    return render(self.request, self.template_name, context={
      'category': MenuCategory.objects.all(),
      'menu': Menu.objects.order_by('-updated_on'),
      'just_added': Menu.objects.filter(date__date=today_date),
      'today': today_date
      })
