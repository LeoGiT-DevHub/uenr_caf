from django.urls import path, include
from .import views


urlpatterns = [
  path('payment/', views.PaymentTableView.as_view(), name='payment'),
  path('revenue/', views.PaymentTableView.as_view(), name='revenue'),
  path('expenses/', views.PaymentTableView.as_view(), name='expenses'),
]