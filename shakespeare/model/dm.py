"""
Domain model

Material contains all data we have including shakespeare texts. A text is taken
to be a specific version of a work. e.g. the 1623 folio of King Richard III.

We may in future add a Work object to refer to 'abstract' work of which a given
text is a version.
"""
import sqlobject

# make sure config is registered
import shakespeare
shakespeare.conf()

from pylons.database import PackageHub
hub = PackageHub('shakespeare')
sqlobject.sqlhub.processConnection = hub.getConnection()

import shakespeare
import shakespeare.cache

# import other sqlobject items
from annotater.model import Annotation
import annotater.model

# note we run this at bottom of module to auto create db tables on import
def createdb():
    Material.createTable(ifNotExists=True)
    Concordance.createTable(ifNotExists=True)
    Statistic.createTable(ifNotExists=True)
    annotater.model.createdb()

def cleandb():
    Statistic.dropTable(ifExists=True)
    Concordance.dropTable(ifExists=True)
    Material.dropTable(ifExists=True)
    annotater.model.cleandb()

def rebuilddb():
    cleandb()
    createdb()

class Material(sqlobject.SQLObject):
    """Material related to Shakespeare (usually text of works and ancillary
    matter such as introductions).

    NB: can not use 'text' as class name as it is an sql reserved word

    @attribute name: a unique name identifying the material
    
    TODO: mutiple creators ??
    """
    
    name = sqlobject.StringCol(alternateID=True)
    title = sqlobject.StringCol(default=None, length=255)
    # creator rather than author to fit with dublin core
    creator = sqlobject.StringCol(default=None, length=255)
    url = sqlobject.StringCol(default=None, length=255)
    notes = sqlobject.StringCol(default=None)

    def get_cache_path(self, format):
        """Get path within cache to data file associated with this material.
        @format: the version ('plain', original='' etc)
        """
        return shakespeare.cache.default.path(self.url, format)

    def get_store_fileobj(self):
        import pkg_resources
        pkg = 'shksprdata'
        # default to plain txt format (TODO: generalise this)
        path = 'texts/%s.txt' % self.name
        fileobj = pkg_resources.resource_stream(pkg, path)
        return fileobj


class Concordance(sqlobject.SQLObject):

    text = sqlobject.ForeignKey('Material')
    word = sqlobject.StringCol(length=50)
    line = sqlobject.IntCol()
    char_index = sqlobject.IntCol()

    word_index = sqlobject.DatabaseIndex('word')
    text_index = sqlobject.DatabaseIndex('text')

class Statistic(sqlobject.SQLObject):

    text = sqlobject.ForeignKey('Material')
    word = sqlobject.StringCol(length=50)
    occurrences = sqlobject.IntCol(default=1)

    word_index = sqlobject.DatabaseIndex('word')
    text_index = sqlobject.DatabaseIndex('text')


# auto create db tables on import
createdb()

