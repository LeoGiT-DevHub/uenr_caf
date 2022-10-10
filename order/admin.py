from django.contrib import admin

from menu.models import Menu
from .models import Cart, Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ("invoice", "due_date", "served", "price", "discount", "payment", "customer_name", "customer_contact",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = ("user", "menu", "price", "discount", "qty", "ordered")
  
  def save_model(self, request, obj, form, change) -> None:
    menu = Menu.objects.get(pk=request.POST['menu'])
    qty = int(request.POST['qty'])
    obj.price = menu.price * qty
    obj.discount = menu.get_discount()
    return super().save_model(request, obj, form, change)