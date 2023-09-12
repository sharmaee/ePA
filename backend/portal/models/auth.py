import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils import timezone

from ._common import PortalModelBase
from portal.utils.send_emails import send_service_email, NotificationType


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    send_service_email(NotificationType.PASSWORD_RESET, reset_password_token)


class UserManager(BaseUserManager):
    def _create_user(self, **kwargs):
        now = timezone.now()
        kwargs = kwargs.copy()
        password = kwargs['password']
        del kwargs['password']
        kwargs['email'] = kwargs.get('email', '')
        kwargs['is_staff'] = kwargs.get('is_staff', False)
        kwargs['is_superuser'] = kwargs.get('is_superuser', False)
        kwargs['is_active'] = kwargs.get('is_active', True)
        if kwargs['email']:
            kwargs['email'] = self.normalize_email(kwargs['email'])
        user = self.model(last_login=now, submission_date=now, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs):
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        kwargs = kwargs.copy()
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(**kwargs)


class ClientCompany(PortalModelBase):
    company_name = models.TextField(blank=True, null=True)
    email_domain = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    number_of_seats = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name


class User(AbstractBaseUser, PermissionsMixin, PortalModelBase):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField('Email address', unique=True, blank=True, null=True)
    is_staff = models.BooleanField('User status', default=False)
    is_active = models.BooleanField('Active', default=False)
    is_email_verified = models.BooleanField('Verified', default=False)
    is_2fa_verified = models.BooleanField('Google Auth Verified', default=False)
    client_company = models.ForeignKey(
        ClientCompany, related_name="user", on_delete=models.CASCADE, blank=True, null=True
    )
    secret_code = models.CharField(max_length=32, blank=True)
    auth_url = models.CharField(max_length=255, blank=True)
    mobapp_id = models.UUIDField(unique=True, default=uuid.uuid1)
    submission_date = models.DateTimeField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        db_table = 'auth__user'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.mobapp_id}'


class BlackListedAccessToken(PortalModelBase):
    access_token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="access_token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("access_token", "user")
