"""
Domain model

Material contains all data we have including shakespeare texts. A text is taken
to be a specific version of a work. e.g. the 1623 folio of King Richard III.

We may in future add a Work object to refer to 'abstract' work of which a given
text is a version.
"""
from pylons import config
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy import orm
from sqlalchemy.orm import relation, backref

# make sure config is registered
import shakespeare
shakespeare.conf()

metadata = MetaData()
Session = orm.scoped_session(orm.sessionmaker(
    autoflush=True,
    transactional=False,
    bind=config['pylons.g'].sa_engine
))

import shakespeare
import shakespeare.cache

# import other sqlobject items
from annotater.model import Annotation
import annotater.model

material_table = Table('material', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.String(255)),
    Column('title', types.String(255)),
    Column('creator', types.String(255)),
    Column('url', types.String(255)),
    Column('notes', types.Text())
    )

# TODO: indices on word and occurences
statistic_table = Table('statistic', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('material_id', types.Integer, ForeignKey('material.id')),
    Column('word', types.String(50)),
    Column('occurrences', types.Integer, default=1),
    )


from ConfigParser import SafeConfigParser



class Material(object):
    """Material related to Shakespeare (usually text of works and ancillary
    matter such as introductions).

    NB: can not use 'text' as class name as it is an sql reserved word

    @attribute name: a unique name identifying the material
    
    TODO: mutiple creators ??
    """

    # TODO: remove (just here for sqlobject bkwards compat)
    @classmethod
    def byName(self, name):
        return self.query.filter_by(name=name).one()
    
    def get_text(self, format=None):
        '''Get text (if any) associated with this material.

        # ignore format for time being
        '''
        import pkg_resources
        pkg = 'shksprdata'
        # default to plain txt format (TODO: generalise this)
        path = 'texts/%s.txt' % self.name
        fileobj = pkg_resources.resource_stream(pkg, path)
        return fileobj

    def get_cache_path(self, format):
        """Get path within cache to data file associated with this material.
        @format: the version ('plain', original='' etc)
        """
        return shakespeare.cache.default.path(self.url, format)

    @classmethod
    def load_from_metadata(self, fileobj):
        cfgp = SafeConfigParser()
        cfgp.readfp(fileobj)
        for section in cfgp.sections():
            try:
                item = Material.byName(section)
            except:
                item = Material(name=section)
            for key, val in cfgp.items(section):
                setattr(item, key, val)

class Statistic(object):
    pass

# Map each domain model class to its corresponding relational table.
mapper = Session.mapper
mapper(Material, material_table)
mapper(Statistic, statistic_table, properties={
    'text':relation(Material, backref='statistics')
    })

