from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LogoutView,
    RegisterView,
    CustomTokenObtainPairView,
    ActivateView,
    GoogleAuthLoginView,
)


auth_urls = [
    path('sign-in/', CustomTokenObtainPairView.as_view()),
    path('sign-in-step2/', GoogleAuthLoginView.as_view()),
    path('sign-in/refresh/', TokenRefreshView.as_view()),
    path('sign-out/', LogoutView.as_view()),
    path('register/', RegisterView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$', ActivateView.as_view()),
]
