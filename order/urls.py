from django.urls import path, include
from . import views


urlpatterns = [
  path('cart/', views.UserCartView.as_view(), name='user_cart'),
  # path('cart/delete/<str:pk>/', views.UserCart.as_view(), name='user_cart'),
  
  path('new/', views.MakeOrderView.as_view(), name='new_order'),
  path('', views.UserOrdersView.as_view(), name='user_orders'),
  path('db', views.OrdersTableView.as_view(), name='orders'),
  path('invoice/<str:pk>/', views.OrderDetailView.as_view(), name='order_invoice'),
  path('update/<str:pk>/', views.UpdateOrderView.as_view(), name='order_update'),
  path('delete/<str:pk>/', views.DeleteOrderView.as_view(), name='order_delete'),
]