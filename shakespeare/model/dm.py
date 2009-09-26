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
    )

resource_table = Table('resource', metadata,
    Column('id', Integer, primary_key=True),
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('format', UnicodeText),
    # url or path
    Column('locator', UnicodeText),
    # types: url, cache, package, disk, inline
    Column('locator_type', UnicodeText, default=u'url'),
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
        if self.resources:
            return self.resources[0].get_stream()

    def get_ftitle(self):
        return self.title + ' (%s)' % self.name

    ftitle = property(get_ftitle)


class Resource(object):
    def get_stream(self):
        '''Get text (if any) associated with this material.

        # ignore format for time being
        '''
        if self.locator_type == u'package':
            package, path = self.locator.split('::')
            import pkg_resources
            fileobj = pkg_resources.resource_stream(package, path)
            return fileobj
        elif self.locator_type == u'inline':
            from StringIO import StringIO
            return StringIO(self.locator)
        elif self.locator_type == u'cache':
            import shakespeare.cache
            cache = shakespeare.cache.default
            fp = cache.path_from_offset(self.locator)
            return open(fp)
        else:
            raise NotImplementedError


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

mapper(Resource, resource_table, properties={
    'material':relation(Material, backref='resources')
    },
    order_by=resource_table.c.id
    )

mapper(Statistic, statistic_table, properties={
    'text':relation(Material, backref='statistics')
    },
    order_by=statistic_table.c.id
    )

