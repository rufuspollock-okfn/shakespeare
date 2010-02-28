import datetime

from sqlalchemy import Table, Column
from sqlalchemy.types import *

from meta import *
from base import DomainObject, JsonType

key_value_table = Table('key_value', metadata,
        Column('ns', UnicodeText, primary_key=True), # namespace
        Column('object_id', UnicodeText, primary_key=True),
        Column('key', UnicodeText, primary_key=True),
        Column('value', JsonType),
        Column('_created', DateTime, default=datetime.datetime.now),
        )


class KeyValue(DomainObject):
    @classmethod
    def upsert(self, pkey, **kwargs):
        kv = self.query.get(pkey)
        if kv is None:
            kv = self(ns=pkey[0], object_id=pkey[1], key=pkey[2])
        for k,v in kwargs.items():
            setattr(kv, k, v)
        return kv


mapper(KeyValue, key_value_table,
    order_by=[key_value_table.c.ns, key_value_table.c.object_id,
        key_value_table.c.key])

