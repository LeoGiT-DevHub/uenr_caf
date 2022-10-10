from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse
from account.models import Staff
from menu.models import Menu
from order.managers import OrderQuerySet

User = settings.AUTH_USER_MODEL


def cart_ref_generator():
  last_cart = Cart.objects.all().order_by('date').last()
  if not last_cart:
    return 'UENR' + str(timezone.now().date().today().year) + str(timezone.now().date().today().month).zfill(2) + '0000'
  ref = last_cart.ref
  cart_ref_int = int(ref[10:14])
  new_cart_ref_int = cart_ref_int + 1
  new_cart_ref = 'UENR' + str(timezone.now().date().today().year) + str(timezone.now().date().today().month).zfill(2) + str(new_cart_ref_int).zfill(2)
  return new_cart_ref


class Cart(models.Model):
  ref = models.CharField(primary_key=True, unique=True, max_length=120, default=cart_ref_generator)
  user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
  menu    = models.ForeignKey(Menu, related_name='cart_menu', on_delete=models.PROTECT)
  price   = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
  discount  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
  qty  = models.PositiveSmallIntegerField(default=1)
  ordered = models.BooleanField(default=False)
  date    = models.DateTimeField(auto_now_add=True)
  updated_on    = models.DateTimeField(auto_now=True)
  
  def __str__(self):
      return self.ref
  
  @property
  def get_amount_to_pay(self):
    return self.price - self.discount
  
  @property
  def get_price(self):
    return self.price*self.qty
  
  @property
  def get_discount(self):
    return self.menu.get_discount() * self.qty


def invoice_generator():
  last_order = Order.objects.all().order_by('date').last()
  if not last_order:
    return 'UENR' + str(timezone.now().date().today().year) + str(timezone.now().date().today().month).zfill(2) + '0000'
  invoice = last_order.invoice
  order_int = int(invoice[10:14])
  new_order_int = order_int + 1
  new_order_invoice = 'UENR' + str(timezone.now().date().today().year) + str(timezone.now().date().today().month).zfill(2) + str(new_order_int).zfill(2)
  return new_order_invoice

class Order(models.Model):
  PAYMENT_METHODS = (
    ('cash', 'Cash'),
    ('e_cash', (
      ('mtn', 'MTN'),
      ('voda', 'Vodafone'),
      ('bank', 'Bank Transfer'),        
    ),),
  )
  invoice = models.CharField(primary_key=True, unique=True, max_length=20, auto_created=True, default=invoice_generator, editable=False)
  cart = models.ManyToManyField(Cart, related_name='cart_ordered')
  customer_name = models.CharField(max_length=100, null=True, blank=True)
  customer_contact = models.CharField(max_length=13, null=True, blank=True)
  customer_email = models.EmailField(null=True, blank=True)
  delivery_address = models.CharField(max_length=250, null=True, blank=True)
  address_description = models.TextField(null=True, blank=True)
  due_date = models.DateTimeField(default=timezone.now)
  served = models.BooleanField(default=False)
  served_by = models.ForeignKey(Staff, related_name='served_orders', on_delete=models.SET_NULL, null=True, blank=True)
  processed_by = models.ForeignKey(User, related_name='user_orders', on_delete=models.SET_NULL, null=True, blank=True)
  payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default=PAYMENT_METHODS[0][0], null=True, blank=True)
  updated_by = models.ForeignKey(Staff, related_name='updated_orders', on_delete=models.SET_NULL, null=True, blank=True)
  updated_on = models.DateTimeField(auto_now=True)
  date = models.DateTimeField(auto_now_add=True)
  
  objects = models.Manager()
  queryset = OrderQuerySet.as_manager()
  
  class Meta:
    ordering = ("-date",)
    
  def __str__(self):
    return self.invoice
    
  def get_absolute_url(self):
    return reverse("order_invoice", kwargs={"pk": self.pk})
      
  def price(self):
    prices=[]
    for cart in self.cart.all():
      prices.append(cart.price*cart.qty)
    return sum(prices)

  def discount(self):
    dicounts=[]
    for cart in self.cart.all():
      dicounts.append(cart.discount*cart.qty)
    return sum(dicounts)
  
  def amount_to_paid(self):
    return self.price()-self.discount()
  
  def payment(self):
    return self.order_payment.amount
  
  def get_payment_status(self):
    if self.payment()==self.amount_to_paid():
      return True
    elif self.payment() < self.amount_to_paid():
      return False
    return None
  
