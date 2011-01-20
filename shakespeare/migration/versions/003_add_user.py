from datetime import datetime
import uuid

from sqlalchemy import *
from migrate import *

from shakespeare.migration.util import wrap_in_transaction


metadata = MetaData(migrate_engine)
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
        Column('meta', UnicodeText),
        )

@wrap_in_transaction
def upgrade():
    user_table.create()

@wrap_in_transaction
def downgrade():
    user_table.drop()

