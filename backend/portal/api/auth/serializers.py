from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.utils import timezone
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from portal.models.auth import User, ClientCompany
from portal.utils.send_emails import send_activation_email, send_ran_out_of_seats, send_not_registered_promo_email

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobapp_id', 'submission_date')
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class RegisterSaveSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_email(self, value):
        email_domain = value.split('@')[1]
        client_company = ClientCompany.objects.filter(email_domain=email_domain).first()
        if not client_company:
            send_not_registered_promo_email(value, self.initial_data['first_name'], self.initial_data['last_name'])
            raise serializers.ValidationError(
                {"email": "We are on it! Check your email to get started with your account."}
            )
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {
                    "email": (
                        "User already exists. Please try signing into your account or,"
                        "if you've forgotten your password, use the 'Forgot Password' option to reset it."
                    )
                }
            )
        client_user_count = User.objects.filter(client_company=client_company).count()
        if client_user_count >= client_company.number_of_seats:
            send_ran_out_of_seats(
                client_company, value, self.initial_data['first_name'], self.initial_data['last_name']
            )
            raise serializers.ValidationError(
                {"email": "Registration failed. Please reach out to your admin to get additional seats. "}
            )
        return value

    def create(self, validated_data):
        client_company = ClientCompany.objects.filter(email_domain=validated_data['email'].split('@')[1]).first()
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False,
            is_email_verified=False,
            submission_date=timezone.now(),
            client_company=client_company,
        )
        user.set_password(validated_data['password'])
        user.save()
        send_activation_email(user)
        return user


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True, validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ('email',)


class CustomTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': 'No active account found with the given credentials',
        'email_not_verified': 'Email wasn\'t verified',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        try:
            self.user = User.objects.filter(email=attrs['email']).get()
            if self.user.check_password(attrs['password']) and not self.user.is_email_verified:
                raise exceptions.AuthenticationFailed(
                    self.error_messages['email_not_verified'],
                    'email_not_verified',
                )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(attrs['password'])

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['otp_app_url'] = self.user.auth_url
        data['setup_key'] = self.user.secret_code
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['second_step'] = settings.ENABLE_2FA

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
