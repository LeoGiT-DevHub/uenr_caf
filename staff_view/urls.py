from django.urls import path, include
from .import views


urlpatterns = [
    path('menu/', include('menu.urls')),
    path('orders/', include('order.urls')),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('analytical/', views.DashboardAnalyticalView.as_view(), name='dashboard_analytical'),
    path('report/', views.DashboardReportView.as_view(), name='dashboard_report'),
    path('report/', views.DashboardView.as_view(), name='report'),
    path('finance/', include('finance.urls')),
    
    
    path('users/', views.DashboardView.as_view(), name='users'),
    path('user/staff/', views.DashboardView.as_view(), name='staff_users'),
    path('user/client/', views.DashboardView.as_view(), name='client_users'),
    
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('todos/', views.TodosView.as_view(), name='todos'),
    path('blank/', views.BlankView.as_view(), name='blank'),
]
