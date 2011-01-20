import re
from datetime import datetime
import uuid

from sqlalchemy import Table, Column
from sqlalchemy.types import *

from meta import *
from base import DomainObject, JsonType

make_uuid = lambda: unicode(uuid.uuid4())

user_table = Table('user', metadata,
        Column('id', UnicodeText, primary_key=True, default=make_uuid),
        Column('openid', UnicodeText, unique=True),
        Column('username', UnicodeText, unique=True),
        Column('fullname', UnicodeText),
        Column('email', UnicodeText, unique=True),
        Column('api_key', UnicodeText, default=make_uuid),
        Column('created', DateTime, default=datetime.now),
        Column('about', UnicodeText),
        Column('meta', JsonType),
        )

class User(DomainObject):
    VALID_USERNAME = re.compile(r"^[a-zA-Z0-9_\-]{3,255}$")

    @property
    def name(self):
        if self.username and self.username != self.openid:
            return self.username
        elif self.fullname:
            return self.fullname
        else:
            return self.openid

    @classmethod
    def by_openid(self, openid):
        return self.query.filter_by(openid=openid).first()

    @classmethod
    def by_username(self, username):
        return self.query.filter_by(username=username).first()
        

mapper(User, user_table,
    order_by=user_table.c.id)

