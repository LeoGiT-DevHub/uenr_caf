from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.urls import reverse


class UserManager(BaseUserManager):
  def create_user(self, email, contact, first_name, other_name, password=None,is_active=True, is_staff=False, is_admin=False, is_superuser=False):
    if not email:
        raise ValueError("Email Required!")
    if not password:
        raise ValueError("Password Required!")
    if not first_name:
        raise ValueError("First Name Required")
    if not other_name:
        raise ValueError("Other Name Required")
    if not contact:
        raise ValueError("Contact Required")
      
    user_obj = self.model(email=self.normalize_email(email))
    user_obj.contact = contact
    user_obj.first_name = first_name
    user_obj.other_name = other_name
    user_obj.set_password(password)
    user_obj.active = is_active
    user_obj.staff = is_staff
    user_obj.admin = is_admin
    user_obj.superuser = is_superuser
    user_obj.save(using=self._db)
    return user_obj

  def create_staff(self, email, contact, first_name, other_name, password=None):
    user = self.create_user(
        email=email, contact=contact, first_name=first_name, other_name=other_name, password=password, is_staff=True,
    )
    return user

  def create_admin(self, email, contact, first_name, other_name, password=None):
    user = self.create_user(
        email=email, contact=contact, first_name=first_name, other_name=other_name, password=password, is_staff=True, is_admin=True
    )
    return user

  def create_superuser(self, email, contact, first_name = "Super User", other_name="Admin", password=None):
    user = self.create_user(
        email=email, contact=contact, first_name=first_name, other_name=other_name, password=password, is_staff=True, is_admin=True, is_superuser=True,
    )
    return user


class User (AbstractBaseUser, PermissionsMixin):
  phone_regex = RegexValidator(regex = r'^(0)\d{9}$', message = 'Phone number must be in the format: 0241301463')
  
  email         = models.EmailField(('email'), unique=True, max_length=150)
  
  contact       = models.CharField(validators=[phone_regex], max_length=13)
  
  first_name    = models.CharField(('First Name'),max_length=100)
  
  other_name    = models.CharField(('Other Names'), max_length=10)

  # USER PERMISSIONS
  active        = models.BooleanField(('Active'),default=True) # Can login
  staff         = models.BooleanField(('Staff'),default=False) # Is a Staff 
  admin         = models.BooleanField(('Admin'),default=False) # Admin | Has administrator permissions
  superuser = models.BooleanField(('Superuser'),default=False) # SupperUser | Has all permissions
  reg_date = models.DateTimeField(('Registration Date'), auto_now_add=True)
  last_login = models.DateTimeField(('Last Login'), auto_now= True)
    

  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['contact']
  
  class Meta:
    db_table = 'auth_user'
    verbose_name = 'user'
    verbose_name_plural = 'users'

  def __str__(self):
    return f"{self.first_name} {self.other_name}"
  
  def get_absolute_url(self):
    return reverse("user_details", kwargs={"pk": self.pk})
      
  
  def get_email(self):
    return self.email

  def get_full_name(self):
    return (f"{self.first_name} {self.other_name}")

  def get_short_name(self):
    return self.first_name

  def has_perm(self, perm, obj=None):
      return True

  def has_module_perms(self, app_label):
      return True
    
  def get_user_cart_pending(self):
    return self.user_cart.filter(ordered=False)

  @property
  def is_staff(self):
      return self.staff

  @property
  def is_admin(self):
      return self.staff

  @property
  def is_superuser(self):
      return self.superuser


class Profile(models.Model):
  user      = models.OneToOneField(User, on_delete=models.CASCADE)
  img       = models.ImageField(("Image"), upload_to='user/profile_imgs')
  

class Staff(models.Model):
  CATEGORY = (
    ('Manager', 'Manager'),
    ('Sales Person', 'Sales Person'),
    ('Finance', 'Finance'),
    ('Cooks', 'Cooks'),
    ('Staff', 'Staff'),
  )
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff_user')
  category = models.CharField(max_length=50, default=CATEGORY[-1], choices=CATEGORY)
  position = models.CharField(('Staff Rank'), max_length=50)
  
  def __str__(self):
    return f"{self.user.get_short_name()} ({self.category})"
    
  @property
  def email(self):
    return self.user.email
  
  @property
  def contact(self):
    return self.user.contact
  
  @property
  def last_login(self):
    return self.user.last_login
  
  