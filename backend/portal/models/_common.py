import re
<<<<<<< HEAD
import xxhash
import datetime
import logging

from tqdm import tqdm
||||||| parent of f33481d (Install dependency and add draft AES256Field)
=======
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
>>>>>>> f33481d (Install dependency and add draft AES256Field)

from django.db import models
from django.db.models.base import ModelBase
from django.contrib.postgres.search import SearchQuery, SearchRank

<<<<<<< HEAD
logger = logging.getLogger(__name__)
||||||| parent of f33481d (Install dependency and add draft AES256Field)
=======
from django.conf import settings


AES_SECRET_KEY = bytes(settings.AES_SECRET_KEY, 'utf-8')
AES_IV = bytes(settings.AES_IV, 'utf-8')
>>>>>>> f33481d (Install dependency and add draft AES256Field)

punctuation_exp = re.compile(r"[\-!:@#$%^&*()|]")
plus_search_exp = re.compile(r" +")


def camelcase_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def prep_search_query(text, gate, exact):
    text = re.sub(punctuation_exp, ' ', text)
    text = re.sub(plus_search_exp, ' ', text)
    if exact:
        text = gate.join([f'{el}' for el in text.split(' ') if el.strip()])
    else:
        text = gate.join([f'{el}:*' for el in text.split(' ') if el.strip()])
    query = SearchQuery(text, search_type='raw')
    return query


class AutoTableNameModel(ModelBase):
    abstract = True

    def __new__(cls, name, bases, attrs):
        """
        Using module name as a prefix for the table name.
        """
        new_class = super().__new__(cls, name, bases, attrs)

        model_module = new_class.__module__.split('portal.models.')[1].replace('.', '_')
        new_table_name = model_module + '__' + camelcase_to_snake(name)
        new_class._meta.db_table = new_table_name
        new_class._meta.original_attrs['db_table'] = new_table_name

        return new_class


class PortalModelBase(models.Model, metaclass=AutoTableNameModel):
    class Meta:
        abstract = True


class SearchQuerySet(models.QuerySet):
    def search(self, text, gate=' & ', exact=False):
        query = prep_search_query(text, gate, exact)

        rank = SearchRank(models.F('search_vector'), query)
        return self.annotate(rank=rank).filter(search_vector=query).order_by('-rank')


def slugify(hashable_text=None):
    if not hashable_text:
        hashable_text = datetime.datetime.now().isoformat()
    return str(xxhash.xxh64(hashable_text).hexdigest())


def custom_bulk_update_or_create(records, model, existing_ids, pk_field, update_fields):
    new_records = set(records.keys()) - set(existing_ids)
    updated_records = set(records.keys()) & set(existing_ids)

    new_entries = []
    updated_entries = []

    for record in tqdm(records.values(), unit=" records"):
        if record[pk_field] in new_records:
            new_entries.append(model(**record))
        elif record[pk_field] in updated_records:
            updated_entries.append(model(**record))

    logger.info(f"Creating {len(new_entries)} new {model.__name__} records")
    model.objects.bulk_create(new_entries)

    logger.info(f"Updating {len(updated_entries)} {model.__name__} records")
    model.objects.bulk_update(updated_entries, update_fields)


def encrypt_data(data):
    data = pad(data, 16)
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
    return base64.b64encode(cipher.encrypt(data)).decode()


def decrypt_data(data):
    data = base64.b64decode(data)
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
    return unpad(cipher.decrypt(data), 16)


class AES256Field(models.BinaryField):
    description = "AES256 encrypted value"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        kwargs['null'] = True
        self.model_class = kwargs.pop('model_class', None)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["blank"]
        del kwargs["null"]
        return name, path, args, kwargs

    def get_prep_value(self, value):
        return encrypt_data(value) 
  
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)

    def to_python(self, value):
        if isinstance(value, self.model_class):
            return value
        if value is None:
            return value
        return decrypt_data(value)
