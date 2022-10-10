from django.shortcuts import render
from django.views import generic

from .models import Expense, Income, OrderPayment

class PaymentTableView(generic.ListView):
  template_name = 'payment_db.html'
  queryset = OrderPayment.objects.all()
  context_object_name = 'payments'


class RevenueTableView(generic.ListView):
  template_name = 'revenue_db.html'
  queryset = Income.objects.all()
  context_object_name = 'revenue'


class ExpensesTableView(generic.ListView):
  template_name = 'expenses_db.html'
  queryset = Expense.objects.all()
  context_object_name = 'expenses'