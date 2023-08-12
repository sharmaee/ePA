import re
import xxhash
import datetime
import logging

from tqdm import tqdm

from django.db import models
from django.db.models.base import ModelBase
from django.contrib.postgres.search import SearchQuery, SearchRank


logger = logging.getLogger(__name__)


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
