from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    LogoutView,
    RegisterView,
    ChangePasswordView,
    UpdateProfileView,
    CustomTokenObtainPairView,
    ActivateView,
    GoogleAuthLoginView,
)


accounts_urls = [
    path('sign-in/', CustomTokenObtainPairView.as_view()),
    path('sign-in-step2/', GoogleAuthLoginView.as_view()),
    path('sign-in/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('sign-out/', LogoutView.as_view()),
    path('register/', RegisterView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view()),
    re_path(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$', ActivateView.as_view()),
]
