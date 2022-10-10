from datetime import datetime, timedelta
from django.contrib import admin
from . models import Menu, MenuCategory

# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "price", "discount", "total_qty", "active_qty", "total_sales", "total_discount", "active")

  
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
  list_display = ("name", "added_by", "updated_by")
  