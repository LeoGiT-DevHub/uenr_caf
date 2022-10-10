from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('staff_view.urls')),
    path('accounts/', include('account.urls')),
    path('', include('user_view.urls')),
    path("paystack", include(('paystack.urls', 'paystack'), namespace='paystack')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "UENR CAFETERIA"
admin.site.site_title = "ADMIN DASHBOARD"
admin.site.index_title = "Welcome to Admin Dashboard"
