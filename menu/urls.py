from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('db/', views.MenuTableView.as_view(), name='all_menu'),
    
    
    path('new/', views.CreateMenuView.as_view(), name='add_menu'),
    path('detail/<str:pk>/', views.MenuDetailView.as_view(), name='menu_details'),
    path('update/<str:pk>/', views.UpdateMenuView.as_view(), name='update_menu'),
    path('delete/<str:pk>/', views.DeleteMenuView.as_view(), name='delete_menu'),
]
