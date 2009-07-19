from sqlalchemy import *
from migrate import *

metadata = MetaData(migrate_engine)

work_table = Table('work', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('title', String(255)),
    Column('creator', String(255)),
    Column('notes', Text),
    )

material_table = Table('material', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('work_id', Integer, ForeignKey('work.id')),
    Column('title', String(255)),
    Column('creator', String(255)),
    Column('notes', Text),
    Column('format', Text),
    # python package it lives in, if any
    Column('src_pkg', Text),
    # url (file or web) or standard (unix) file path
    Column('src_locator', Text),
    )

statistic_table = Table('statistic', metadata,
    Column('id', Integer, primary_key=True),
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('word', String(50)),
    Column('freq', Integer),
    )

def upgrade():
    metadata.create_all()

def downgrade():
    metadata.drop_all()

