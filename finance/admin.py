from django.contrib import admin
from .models import OrderPayment, Expense, Income

# Register your models here.
@admin.register(OrderPayment)
class OrderAdmin(admin.ModelAdmin):
  list_display = ("ref", "paid_for", "amount", "paid_by")


@admin.register(Expense)
class CartAdmin(admin.ModelAdmin):
  list_display = ("ref", "amount", "purpose", "approved")
  
@admin.register(Income)
class CartAdmin(admin.ModelAdmin):
  list_display = ("ref", "amount", "income_from")
  