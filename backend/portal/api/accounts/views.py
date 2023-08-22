import pyotp
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import status

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from portal.api.utils import IsTokenValid
from portal.models.accounts import User, BlackListedAccessToken
from portal.utils.token import account_activation_token
from portal.exceptions import PortalException
from .serializers import (
    RegisterSerializer,
    RegisterSaveSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
    ResetPasswordSaveSerializer,
    CustomTokenObtainPairSerializer,
)


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(RegisterSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)


class GoogleAuthLoginView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            totp = pyotp.TOTP(user.secret_code)
            if totp.verify(request.data.get('code')):
                user.is_2fa_verified = True
                user.save()
                response = {'status': 'success', 'code': status.HTTP_200_OK, 'message': 'Code accepted'}
                return Response(response)

            return Response(
                {'status': 'failure', "code": status.HTTP_401_UNAUTHORIZED, 'message': 'Wrong code'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    def post(self, request):
        try:
            user = request.user
            user.is_2fa_verified = False
            user.save()
            access_token = request.auth.token.decode("utf-8")
            BlackListedAccessToken.objects.create(user=user, access_token=access_token, timestamp=timezone.now())
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(request.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(request.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(UpdateAPIView):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = ResetPasswordSaveSerializer


class UpdateProfileView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


class ActivateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_active:
                raise PortalException('This user is already activated')

            user.is_active = True
            user.is_email_verified = True
            secret_code = pyotp.random_base32()
            user.secret_code = secret_code
            user.auth_url = pyotp.totp.TOTP(secret_code).provisioning_uri(
                name=user.email, issuer_name=settings.ISSUER_NAME
            )
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can log into your account.')
        else:
            raise PortalException('Activation token is invalid!')


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer
