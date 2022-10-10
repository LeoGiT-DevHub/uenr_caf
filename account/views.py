
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic

from .models import User

from .form import LoginForm, RegistrationForm

class SignUpView(SuccessMessageMixin, generic.CreateView):
  template_name = 'signup.html'
  form_class = RegistrationForm
  success_url = reverse_lazy('home')
  context_object_name = 'form'
  success_message = "Your account was created successfully"
  
  def get(self, request):
    # if request.user.is_authenticated:
    #   if self.request.GET.get('next'):
    #     return redirect(self.request.GET.get('next'))
    #   return redirect('dashboard')
    form = self.form_class()
    message = 'Just Visited / Refreshed'
    return render(request, self.template_name, context={'form': form, 'message': message})
        
  def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
      form.save()
      user = authenticate(
        email=form.cleaned_data['email'],
        password=form.cleaned_data['password1'],
      )
      if user is not None:
        login(request, user)
        if self.request.GET.get('next'):
          return redirect(self.request.GET.get('next'))
        if request.user.is_staff:
          return redirect('dashboard')
        if request.user.is_admin:
          return redirect('admin')
        return redirect('home')
      message = 'Login failed!'
      return render(request, self.template_name, context={'form': form, 'message': message})
            
    else:
      form = self.form_class
      message = 'Invalid Form. Ensure all the fields have been filled with the needed info'
      return render(request, self.template_name, context={'form': form, 'message': message})


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url: reverse_lazy('home')
    
    def get(self, request):
        if request.user.is_authenticated:
          if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
          if request.user.is_admin:
            return redirect('admin:index')
          if request.user.is_staff:
            return redirect('dashboard')
          return redirect('home')
        form = self.form_class()
        message = 'Login failed. Email and/or password incorrect'
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
              login(request, user)
              if self.request.GET.get('next'):
                return redirect(self.request.GET.get('next'))
              return redirect('dashboard')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class ProfileView(LoginRequiredMixin, generic.DetailView):
  template_name = 'user_details.html'
  model = User
  form_class = RegistrationForm
  success_url = reverse_lazy('home')
  

class LogoutView(LoginRequiredMixin, generic.View):
  model = User
  success_url = reverse_lazy('home')
  
  def get(self, request):
    if request.user.is_authenticated:
      logout(request)
      return redirect('home')
    

class ChangePWDView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
  template_name = 'change_pwd.html'
  model = User
  form_class = RegistrationForm
  success_url = reverse_lazy('home')


class ResetPWDView(LoginRequiredMixin, SuccessMessageMixin, generic.FormView):
  template_name = 'pwd_reset.html'
  model = User
  success_url = reverse_lazy('home')
