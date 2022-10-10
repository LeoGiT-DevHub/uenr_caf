from django.db import models
from django.conf import settings

from account.models import Staff
from finance.managers import OrderPaymentQuerySet
from order.models import Order

User = settings.AUTH_USER_MODEL

class OrderPayment(models.Model):
  PAYMENT_METHODS = (
    ('cash', 'Cash'),
    ('e_cash', (
      ('mtn', 'MTN'),
      ('voda', 'Vodafone'),
      ('bank', 'Bank Transfer'),        
    ),),
  )
  ref = models.CharField(max_length=60)
  paid_for = models.OneToOneField(
    Order,
    on_delete=models.PROTECT,
    related_name="order_payment"
  )
  amount = models.DecimalField(
    decimal_places=2,
    max_digits=10
  )
  paid_with = models.CharField(
    max_length=50,
    default=PAYMENT_METHODS[0][0],
    choices=PAYMENT_METHODS
  )
  paid_by = models.CharField(max_length=150, null=True, blank=True)
  through = models.ForeignKey(
    User, 
    on_delete=models.SET_NULL, 
    null=True, blank=True, 
    related_name='paid_through'
  )
  date = models.DateTimeField(auto_now_add=True)

  objects = models.Manager()
  queryset = OrderPaymentQuerySet.as_manager()
  
  class Meta:
    ordering = ('-date',)

  def __str__(self):
    return self.ref

  def get_status(self):
    return self.paid_for.get_payment_status()
  
 
class Expense(models.Model):
  ref = models.CharField(max_length=60)
  amount = models.DecimalField(decimal_places=2, max_digits=10)
  purpose = models.CharField(max_length=250)
  details = models.TextField()
  approved = models.BooleanField(default=False)
  by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)

  objects = models.Manager()
  queryset = OrderPaymentQuerySet.as_manager()
  
  def __str__(self):
    return self.ref
  

class Income(models.Model):
  ref = models.CharField(max_length=60)
  amount = models.DecimalField(decimal_places=2, max_digits=10)
  income_from = models.CharField(max_length=250)
  details = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  objects = models.Manager()
  queryset = OrderPaymentQuerySet.as_manager()
  
  def __str__(self):
    return self.ref
  
  