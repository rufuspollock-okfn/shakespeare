"""
Domain model

Material contains all data we have including Milton texts. 

We may in future add a Work object to refer to 'abstract' work of which a given
text is a version.
"""
import sqlobject

import milton
import milton.cache

uri = milton.conf().get('db', 'uri')
connection = sqlobject.connectionForURI(uri)
sqlobject.sqlhub.processConnection = connection

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
    """Material related to milton (usually text of works and ancillary
    matter such as introductions).

    NB: can not use 'text' as class name as it is an sql reserved word

    @attribute name: a unique name identifying the material
    
    TODO: mutiple creators ??
    """
    
    name = sqlobject.StringCol(alternateID=True, length=255)
    title = sqlobject.StringCol(default=None, length=255)
    # creator rather than author to fit with dublin core
    creator = sqlobject.StringCol(default=None, length=255)
    url = sqlobject.StringCol(default=None, length=255)
    notes = sqlobject.StringCol(default=None)

    def get_cache_path(self, format):
        """Get path within cache to data file associated with this material.
        @format: the version ('plain', original='' etc)
        """
        return e.default.path(self.url, format)

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

