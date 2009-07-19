"""
Domain model
"""
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import *
from sqlalchemy.orm import relation, backref

from meta import *

import shakespeare

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

# TODO: indices on word and occurences
statistic_table = Table('statistic', metadata,
    Column('id', Integer, primary_key=True),
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('word', Unicode(50)),
    Column('freq', Integer),
    )


class Work(object):

    @classmethod
    def by_name(self, name):
        return self.query.filter_by(name=name).first()

class Material(object):
    """Material related to Shakespeare (usually text of works and ancillary
    matter such as introductions).

    NB: can not use 'text' as class name as it is an sql reserved word

    @attribute name: a unique name identifying the material
    
    TODO: mutiple creators ??
    """

    # TODO: remove (just here for sqlobject bkwards compat)
    @classmethod
    def by_name(self, name):
        return self.query.filter_by(name=name).first()

    @classmethod
    def byName(self, name):
        return self.by_name(name)
    
    def get_text(self, format=None):
        '''Get text (if any) associated with this material.

        # ignore format for time being
        '''
        import pkg_resources
        # default to plain txt format (TODO: generalise this)
        fileobj = pkg_resources.resource_stream(self.src_pkg, self.src_locator)
        return fileobj

    def get_ftitle(self):
        return self.title + ' (%s)' % self.name

    ftitle = property(get_ftitle)


class Statistic(object):
    pass

# Map each domain model class to its corresponding relational table.
mapper = Session.mapper

mapper(Work, work_table,
    order_by=work_table.c.name
    )

mapper(Material, material_table, properties={
    'work':relation(Work, backref='materials')
    },
    order_by=material_table.c.name
    )

mapper(Statistic, statistic_table, properties={
    'text':relation(Material, backref='statistics')
    },
    order_by=statistic_table.c.id
    )

