"""
Domain model

Material contains all data we have including shakespeare texts. A text is taken
to be a specific version of a work. e.g. the 1623 folio of King Richard III.

We may in future add a Work object to refer to 'abstract' work of which a given
text is a version.
"""
import sqlobject

import shakespeare

uri = shakespeare.conf().get('db', 'uri')
__connection__ = sqlobject.connectionForURI(uri)

# note we run this at bottom of module to auto create db tables on import
def createdb():
    Material.createTable(ifNotExists=True)
    Concordance.createTable(ifNotExists=True)

def cleandb():
    Concordance.dropTable(ifExists=True)
    Material.dropTable(ifExists=True)

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
    # creator rather than author to fit with dc
    creator = sqlobject.StringCol(default=None, length=255)
    cache_path = sqlobject.StringCol(default=None, length=255)
    notes = sqlobject.StringCol(default=None)

class Concordance(sqlobject.SQLObject):

    text = sqlobject.ForeignKey('Material')
    word = sqlobject.StringCol(length=50)
    line = sqlobject.IntCol()
    char_index = sqlobject.IntCol()

    word_index = sqlobject.DatabaseIndex('word')
    text_index = sqlobject.DatabaseIndex('text')


# auto create db tables on import
createdb()

