from sqlalchemy import *
from migrate import *

metadata = MetaData(migrate_engine)

work_table = Table('work', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(255)),
    Column('title', Unicode(255)),
    Column('creator', Unicode(255)),
    Column('notes', UnicodeText),
    )

material_table = Table('material', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(255)),
    Column('work_id', Integer, ForeignKey('work.id')),
    Column('title', Unicode(255)),
    Column('creator', Unicode(255)),
    Column('notes', UnicodeText),
    Column('format', UnicodeText),
    # python package it lives in, if any
    Column('src_pkg', UnicodeText),
    # url (file or web) or standard (unix) file path
    Column('src_locator', UnicodeText),
    )

statistic_table = Table('statistic', metadata,
    Column('id', Integer, primary_key=True),
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('word', Unicode(50)),
    Column('freq', Integer),
    )

def upgrade():
    metadata.create_all()

def downgrade():
    metadata.drop_all()

