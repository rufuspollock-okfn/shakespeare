from datetime import datetime
import uuid

from sqlalchemy import Table, Column
from sqlalchemy.types import *

from meta import *
from base import DomainObject

make_uuid = lambda: unicode(uuid.uuid4())

user_table = Table('user', metadata,
        Column('id', UnicodeText, primary_key=True, default=make_uuid),
        Column('name', UnicodeText, unique=True),
        Column('email', UnicodeText, unique=True),
        Column('api_key', UnicodeText, default=make_uuid),
        Column('created', DateTime, default=datetime.now),
        Column('about', UnicodeText),
        )

class User(DomainObject):
    pass

mapper(User, user_table,
    order_by=user_table.c.name)

