import re
import xxhash
import datetime

from django.db import models
from django.db.models.base import ModelBase
from django.contrib.postgres.search import SearchQuery, SearchRank


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


def generate_url_slug():
    return str(xxhash.xxh64(datetime.datetime.now().isoformat()).hexdigest())
