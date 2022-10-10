from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormMixin

from order.forms import CartForm
from order.models import Cart
from .form import MenuForm
from .models import Menu, MenuCategory

today_date = date.today()

class CreateMenuView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
  template_name = 'menu_form.html'
  success_url = reverse_lazy('menu_detail')
  form_class = MenuForm
  
  def test_func(self):
    return self.request.user.is_staff
      
  def get_context_data(self, **kwargs):
    context = super(CreateMenuView, self).get_context_data(**kwargs)
    context.update({
      'category': MenuCategory.objects.all(),
      'menu': Menu.objects.all(),
      # 'active_menu': Menu.objects.filter(get_active_bool = True),
    })
    return context

  def post(self, request):
    form = MenuForm(request.POST, request.FILES)
    if form.is_valid():
      menu = form.save(commit=False)
      menu.added_by = request.user.staff_user
      menu.updated_by = request.user.staff_user
      menu.save()
      messages.success(self.request, f"{menu.name} Created Successfully !")
      return redirect('menu_details', menu.pk)
    
    for error in list(form.errors.values()):
      messages.error(self.request, error)
                     
    return render(request, self.template_name, context={'form':form})


class MenuView(SuccessMessageMixin, generic.ListView):  
  template_name = 'menu.html'
  queryset = Menu.objects.order_by('-updated_on')
  context_object_name = 'menu'
    
  def get_context_data(self, **kwargs):
    context = super(MenuView, self).get_context_data(**kwargs)
    context.update({
      'category': MenuCategory.objects.all(),
      'just_added': Menu.objects.filter(date__date=today_date),
      'today': today_date
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
      cart = Cart.objects.get(user=user, ordered=False, menu=menu or buy_now)
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

 
class MenuTableView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.ListView):
  template_name = 'menu_db.html'
  queryset = Menu.objects.all()
  context_object_name = 'all_menu'
  
  def test_func(self):
    return self.request.user.is_staff
  
  def get_context_data(self, **kwargs):
    context = super(MenuTableView, self).get_context_data(**kwargs)
    context.update({
      'category': MenuCategory.objects.all(),
      # 'active_menu': Menu.objects.filter(get_active_bool = True),
      'just_added':Menu.objects.filter(date__date=today_date),
    })
    return context

 
class MenuDetailView(SuccessMessageMixin, generic.DetailView):
  template_name = 'menu_detail.html'
  model = Menu
  context_object_name = 'menu'
    
  def get_context_data(self, **kwargs):
    context = super(MenuDetailView, self).get_context_data(**kwargs)
    context.update({
      'today_menu_sales': self.model.queryset.today(),
      'this_week_menu_sales': self.model.queryset.this_week(),
      'this_month_menu_sales': self.model.queryset.this_month(),
      'this_year_menu_sales': self.model.queryset.this_year(),
    })
    return context 


class UpdateMenuView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
  template_name = 'menu_form.html'
  model = Menu
  form_class = MenuForm
  success_message = "Menu Updated successfully"
  
  def test_func(self):
    return self.request.user.is_staff
 
  # def post(self, request):
  #   form = MenuForm(request.POST)
  #   if form.is_valid():
  #     menu = form.save(commit=False)
  #     menu.updated_by = request.user.staff_user
  #     menu.save()
  #     return redirect('menu_detail')
      
  #   return render(request, self.template_name, context={'form':form})
  

class DeleteMenuView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
  template_name = 'confirm_delete.html'
  model = Menu
  success_url = reverse_lazy('all_menu')
  success_message = "Menu Deteled successfully"
  
  def test_func(self):
    return self.request.user.is_staff
