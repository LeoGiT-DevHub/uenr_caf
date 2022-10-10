from datetime import date, datetime, timedelta
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse

from account.models import Staff
from menu.managers import MenuQuerySet

today_date = date.today()
User = settings.AUTH_USER_MODEL

class MenuCategory(models.Model):
  name = models.CharField(max_length=100, unique=True, primary_key=True)
  description = models.TextField()
  added_by = models.ForeignKey(Staff, related_name="menu_cat_added_by", on_delete=models.SET_NULL, null=True, blank=True)
  updated_by = models.ForeignKey(Staff, related_name="menu_cat_updated_by", on_delete=models.SET_NULL, null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.name.split(' ')[0]
   
class Menu(models.Model):
  img = models.ImageField(upload_to='menu/images/')
  name  = models.CharField(max_length=200, unique=True)
  category  = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_category')
  detail = models.TextField(null=True, blank=True)
  price = models.DecimalField(decimal_places=2, max_digits=10)
  discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
  qty = models.SmallIntegerField(default=0)
  total_qty = models.BigIntegerField(default=0, editable=False)
  # active = models.BooleanField(default=False)

  # # SECURITY DATA FIELD
  added_by    = models.ForeignKey(Staff, related_name='menu_added_by', on_delete=models.SET_NULL, null=True, blank=True)
  updated_by = models.ForeignKey(Staff, related_name='menu_updated_by', on_delete=models.SET_NULL, null=True, blank=True)
  updated_on = models.DateTimeField(auto_now=True)
  date  = models.DateTimeField(auto_now_add=True)
  
  objects = models.Manager()
  queryset = MenuQuerySet.as_manager()
  
  class Meta:
    ordering = ("-date",)
    
  def save(self, *args, **kwargs):
    if not self.id:
      self.date = timezone.now()
    self.total_qty += self.qty
    self.qty = 0
    super(Menu, self).save(*args, **kwargs) # Call the real save() method   
    
  def __str__(self):
   return f"{self.name} ({self.category})"
 
  def get_absolute_url(self):
    return reverse("menu_details", kwargs={"pk": self.pk})
  
  def active(self):
    if self.updated_on.date() == date.today():
      if self.total_qty > self.get_sold_count():
        return True 
    return False

  def active_qty(self):
    return self.total_qty-self.get_sold_count()

  def get_sold_count(self):
    cart_qty =[]
    sold=self.cart_menu.filter(ordered=True)
    for cart in sold:
      cart_qty.append(cart.qty)
    return sum(cart_qty)

        
  def get_discount(self):
    return ((self.discount/100) * self.price)
  
  def get_amount_to_pay(self):
    return self.price-self.get_discount()
        
  def total_discount(self):
    cart_discounts =[]
    sold=self.cart_menu.filter(ordered=True)
    for cart in sold:
      cart_discounts.append(cart.discount)
    return sum(cart_discounts)

  def total_sales(self):
    cart_prices =[]
    sold=self.cart_menu.filter(ordered=True)
    for cart in sold:
      cart_prices.append(cart.price)
    return (sum(cart_prices) - self.total_discount())
          
  def get_total_sales(self):
    prices = []
    qtys = []
    disc = []
    cart_dict = {}
    
    for cart in self.cart_menu.filter(ordered=True):
      prices.append(cart.price)   
      qtys.append(cart.qty)
      disc.append(cart.discount)
    
    cart_dict.update([('amount', sum(prices)), ('disc', sum(disc)), ('qty', sum(qtys))])
    return cart_dict
          
  def get_today_sales(self):
    prices = []
    qtys = []
    disc = []
    cart_dict = {}
    
    for cart in self.cart_menu.filter(ordered=True, updated_on__date=today_date):
      prices.append(cart.price)   
      qtys.append(cart.qty)
      disc.append(cart.discount)
    
    cart_dict.update([('amount', sum(prices)), ('disc', sum(disc)), ('qty', sum(qtys))])
    return cart_dict
          
  def get_this_week_sales(self):
    prices = []
    qtys = []
    disc = []
    cart_dict = {}
    
    for cart in self.cart_menu.filter(
      ordered=True,
      updated_on__date__iso_week_day__gte= 1,
      updated_on__date__iso_week_day__lt= 7,
      updated_on__date__month = today_date.month,
      updated_on__date__year = today_date.year,
    ):
      prices.append(cart.price)   
      qtys.append(cart.qty)
      disc.append(cart.discount)
    
    cart_dict.update([('amount', sum(prices)), ('disc', sum(disc)), ('qty', sum(qtys))])
    return cart_dict
    
  def get_this_month_sales(self):
    prices = []
    qtys = []
    disc = []
    cart_dict = {}
    
    for cart in self.cart_menu.filter(
      ordered=True,
      updated_on__month = today_date.month,
      updated_on__year = today_date.year
    ):
      prices.append(cart.price)   
      qtys.append(cart.qty)
      disc.append(cart.discount)
    
    cart_dict.update([('amount', sum(prices)), ('disc', sum(disc)), ('qty', sum(qtys))])
    return cart_dict

  def get_this_year_sales(self):
    prices = []
    qtys = []
    disc = []
    cart_dict = {}
    
    for cart in self.cart_menu.filter(
      ordered=True,
      updated_on__year = today_date.year
    ):
      prices.append(cart.price)   
      qtys.append(cart.qty)
      disc.append(cart.discount)
    
    cart_dict.update([('amount', sum(prices)), ('disc', sum(disc)), ('qty', sum(qtys))])
    return cart_dict

