import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from django.db import models
from django.utils.encoding import smart_str
from django.conf import settings


AES_SECRET_KEY = bytes(settings.AES_SECRET_KEY, 'utf-8')
AES_IV = bytes(settings.AES_IV, 'utf-8')


class AES256EncryptedField(models.TextField):
    description = "AES256 encrypted value"

    def __init__(self, *args, **kwargs):
        self.aes_prefix = smart_str(kwargs.pop('aes_prefix', u'aes:'))
        if not self.aes_prefix:
            raise ValueError('AES Prefix cannot be null.')
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["blank"]
        del kwargs["null"]
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if not value:
            return value

        return self.aes_prefix + self._encrypt(value)

    def from_db_value(self, value, expression, connection):
        if value and not value.startswith(self.aes_prefix):
            return value
        if value is None:
            return value
        return self._decrypt(value[len(self.aes_prefix) :])

    def to_python(self, value):
        if value and not value.startswith(self.aes_prefix):
            return value
        if value is None:
            return value
        return self._decrypt(value[len(self.aes_prefix) :])

    def _encrypt(self, data):
        data = pad(data.encode(), 16)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
        return base64.b64encode(cipher.encrypt(data)).decode()

    def _decrypt(self, data):
        data = base64.b64decode(data)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
        if data:
            return unpad(cipher.decrypt(data), 16).decode()
