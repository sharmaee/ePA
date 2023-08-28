import os
from django.core.management import CommandError
from django.contrib.auth.management.commands import createsuperuser
from django.db import DEFAULT_DB_ALIAS
from django.conf import settings


class Command(createsuperuser.Command):
    help = 'Crate/update a superuser based on details provided in local settings'

    def add_arguments(self, _):
        pass

    def handle(self, *args, **options):
        username = settings.SUPERUSER_USERNAME
        password = settings.SUPERUSER_PASSWORD
        email = settings.DEFAULT_TO_EMAIL

        if not password or not username:
            raise CommandError("Please, specify SUPERUSER_USERNAME and SUPERUSER_PASSWORD in your settings")

        options[self.UserModel.USERNAME_FIELD] = username
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = password

        options['interactive'] = False
        options['verbosity'] = 1
        options['database'] = DEFAULT_DB_ALIAS
        options['email'] = email

        try:
            super().handle(*args, **options)
        except CommandError as e:
            if 'already taken' not in str(e):
                raise e

            self.stdout.write("Superuser exists. Updating the password.")
            user = self.UserModel._default_manager.db_manager(options['database']).get_by_natural_key(username)
            user.set_password(password)
            user.save()
