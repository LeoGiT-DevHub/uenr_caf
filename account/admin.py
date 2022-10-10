from django.contrib import admin
from .models import User, Staff, Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ("__str__", "email", "contact", "last_login", "is_staff", "is_admin")
  

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
  list_display = ("__str__", "email", "contact", "last_login", "position")


admin.site.register(Profile)