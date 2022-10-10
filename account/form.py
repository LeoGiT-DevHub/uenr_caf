from django import forms
from django.forms import ModelForm
from .models import User

from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["first_name"].widget.attrs.update({
      'required':'',
      'id':'first_name',
      'type':'text',
      'name':'firs_tname',
      'placeholder':'First Name',
      'class':'form-control bg-white border-left-0 border-md'
    })
    self.fields["other_name"].widget.attrs.update({
      'required':'',
      'id':'other_name',
      'type':'text',
      'name':'other_name',
      'placeholder':'other_name',
      'class':'form-control bg-white border-left-0 border-md'
    })
    self.fields["email"].widget.attrs.update({
      'required':'',
      'id':'email',
      'type':'text',
      'name':'email',
      'placeholder':'Email Address',
      'class':'form-control bg-white border-left-0 border-md'
    })
    self.fields["contact"].widget.attrs.update({
      'required':'',
      'id':'phone_number',
      'type':'tel',
      'name':'contact',
      'placeholder':'Phone Number',
      'class':'form-control bg-white border-md border-left-0 pl-3'
    })
    self.fields["password1"].widget.attrs.update({
      'required':'',
      'id':'password1',
      'type':'text',
      'name':'password1',
      'placeholder':'Password',
      'class':'form-control bg-white border-left-0 border-md'
    })
    self.fields["password2"].widget.attrs.update({
      'required':'',
      'id':'password2',
      'type':'text',
      'name':'password2',
      'placeholder':'Confirm Password',
      'class':'form-control bg-white border-left-0 border-md'
    })
      
  class Meta:
    model = User
    fields = ("first_name","other_name", "email", "contact", "password1", "password2")
  
  
class LoginForm(forms.Form):
  email = forms.CharField(max_length=63)
  password = forms.CharField(max_length=63, widget=forms.PasswordInput)
    
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["email"].widget.attrs.update({
      'required':'',
      'id':'email',
      'type':'text',
      'name':'email',
      'placeholder':'Email Address',
      'class':'form-control bg-white border-left-0 border-md'
    })
    self.fields["password"].widget.attrs.update({
      'required':'',
      'id':'password1',
      'type':'text',
      'name':'password',
      'placeholder':'Password',
      'class':'form-control bg-white border-left-0 border-md'
    })
    
    
    