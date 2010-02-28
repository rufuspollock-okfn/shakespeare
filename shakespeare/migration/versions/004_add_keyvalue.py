import datetime

from sqlalchemy import *
from migrate import *

from shakespeare.migration.util import wrap_in_transaction


metadata = MetaData(migrate_engine)

key_value_table = Table('key_value', metadata,
        Column('ns', UnicodeText, primary_key=True), # namespace
        Column('object_id', UnicodeText, primary_key=True),
        Column('key', UnicodeText, primary_key=True),
        # actually a JsonType but for DB purposes this is just UnicodeText
        Column('value', UnicodeText),
        Column('_created', DateTime, default=datetime.datetime.now),
        )

@wrap_in_transaction
def upgrade():
    key_value_table.create()

@wrap_in_transaction
def downgrade():
    key_value_table.drop()

