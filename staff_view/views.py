from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic
from finance.models import Income, OrderPayment
from menu.models import Menu, MenuCategory

from order.models import Cart, Order

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'dashboard_basic.html'
  
  def test_func(self):
    return self.request.user.is_staff
  
  def get_orders(self, period, served=None):
    orders = Order.queryset.query_period(period, served) 

    prices =[]
    discounts = []
    order_dict = {}
    count = 0
    
    if orders:
      count = orders.count()
      for item in orders:
        prices.append(item.price())
        discounts.append(item.discount())
    
    order_dict.update([('count', count), ('amount', sum(prices)), ('discount', sum(discounts))])
    return order_dict  
 
  def get_payment(self, period, paid_with=None):
    payments = OrderPayment.queryset.query_period(period, paid_with)
    prices =[]
    count = 0
    payment_dict = {}
    
    if payments:
      count = payments.count()
      for item in payments:
        prices.append(item.amount)
    
    payment_dict.update([('count', count), ('amount', sum(prices))])
    return payment_dict
 
  def get_revenue(self, period, paid_with=None):
    revenue = Income.queryset.query_period(period, paid_with)
    prices =[]
    count = 0
    revenue_dict = {}
    
    if revenue:
      count = revenue.count()
      for item in revenue:
        prices.append(item.amount)
    
    revenue_dict.update([('count', count), ('amount', sum(prices))])
    return revenue_dict
 
  def get_expenses(self, period, paid_with=None):
    payments = OrderPayment.queryset.query_period(period, paid_with)
    prices =[]
    count = 0
    payment_dict = {}
    
    if payments:
      count = payments.count()
      for item in payments:
        prices.append(item.amount)
    
    payment_dict.update([('count', count), ('amount', sum(prices))])
    return payment_dict
 
  def get_context_data(self, **kwargs):
    context = super(DashboardView, self).get_context_data(**kwargs)
    context.update({
      'orders': self.get_orders(period = self.request.GET.get('filter_period')),
      'served_orders': self.get_orders(period = self.request.GET.get('filter_period'), served=True),
      'pending_orders': self.get_orders(period = self.request.GET.get('filter_period'), served=False),
      
      'revenue': self.get_revenue(period = self.request.GET.get('filter_period')),
      'cash_payment': self.get_payment(period = self.request.GET.get('filter_period'), paid_with='cash'),
      'e_payment': self.get_payment(period = self.request.GET.get('filter_period'), paid_with='e_cash'),
      
      'payment': self.get_payment(period = self.request.GET.get('filter_period')),
      'cash_payment': self.get_payment(period = self.request.GET.get('filter_period'), paid_with='cash'),
      'e_payment': self.get_payment(period = self.request.GET.get('filter_period'), paid_with='e_cash'),
      
      'all_menu': Menu.objects.all(),
      'menu_cat': MenuCategory.objects.all(),
      'user_cart': Cart.objects.filter(user = self.request.user, ordered = False),
      'user_orders': Order.objects.filter(processed_by = self.request.user),
    })
    return context


class DashboardAnalyticalView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
   
  def test_func(self):
    return self.request.user.is_staff
 

class DashboardReportView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
    
  def test_func(self):
    return self.request.user.is_staff
 

class CalendarView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/calendar.html'
  
  def test_func(self):
    return self.request.user.is_staff

class TodosView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/todos.html'
  
  def test_func(self):
    return self.request.user.is_staff

class BlankView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
  
  def test_func(self):
    return self.request.user.is_staff

class HelpDiskHomeView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
  
  def test_func(self):
    return self.request.user.is_staff

class HelpDiskIssuesView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
  
  def test_func(self):
    return self.request.user.is_staff

class HelpDiskQAsView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
  template_name = 'utils/blank_page.html'
  
  def test_func(self):
    return self.request.user.is_staff