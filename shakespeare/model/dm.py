"""
Domain model
"""
from pylons import config
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy import orm
from sqlalchemy.orm import relation, backref

# make sure config is registered
import shakespeare
shakespeare.conf()

metadata = MetaData(bind=config['pylons.g'].sa_engine)
Session = orm.scoped_session(orm.sessionmaker(
    autoflush=True,
    transactional=False,
    bind=config['pylons.g'].sa_engine
))

import shakespeare
import shakespeare.cache


material_table = Table('material', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.String(255)),
    Column('title', types.String(255)),
    Column('creator', types.String(255)),
    # TODO: remove url
    Column('url', types.String(255)),
    Column('notes', types.Text),
    Column('format', types.Text),
    # python package it lives in, if any
    Column('src_pkg', types.Text),
    # url (file or web) or standard (unix) file path
    Column('src_locator', types.Text),
    )

# TODO: indices on word and occurences
statistic_table = Table('statistic', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('material_id', types.Integer, ForeignKey('material.id')),
    Column('word', types.String(50)),
    Column('freq', types.Integer),
    )


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

    def get_cache_path(self, format):
        """Get path within cache to data file associated with this material.
        @format: the version ('plain', original='' etc)
        """
        return shakespeare.cache.default.path(self.url, format)

    def get_ftitle(self):
        return self.title + ' (%s)' % self.name

    ftitle = property(get_ftitle)


class Statistic(object):
    pass

# Map each domain model class to its corresponding relational table.
mapper = Session.mapper
mapper(Material, material_table,
    order_by=material_table.c.name
    )
mapper(Statistic, statistic_table, properties={
    'text':relation(Material, backref='statistics')
    },
    order_by=statistic_table.c.id
    )

