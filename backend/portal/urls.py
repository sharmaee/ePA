from django.urls import path, include
from django.contrib import admin

from portal.api.urls import api_url_patterns

from django_otp.admin import OTPAdminSite
  
admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('admin-iMNE4Dm9tkm1/', admin.site.urls),
    path('api/', include(api_url_patterns)),
]
