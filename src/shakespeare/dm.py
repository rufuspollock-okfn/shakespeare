"""
Domain model

WorkText refers to a specific version of a work. e.g. the 1623 folio of King
Richard III.

We may in future add a Work object to refer to 'abstract' work of which a given
text is a version.
"""
import sqlobject

import shakespeare

uri = shakespeare.conf().get('db', 'uri')
__connection__ = sqlobject.connectionForURI(uri)

def createdb():
    WorkText.createTable(ifNotExists=True)
    Concordance.createTable(ifNotExists=True)

def dropdb():
    WorkText.dropTable(ifExists=True)
    Concordance.dropTable(ifExists=True)

def rebuilddb():
    dropdb()
    createdb()

# text is a reserved word
class WorkText(sqlobject.SQLObject):
    
    name = sqlobject.StringCol(alternateID=True)
    'idname is unique identifying string e.g. hamlet_1623'
    title = sqlobject.StringCol()
    author = sqlobject.StringCol(default=None)
    notes = sqlobject.StringCol(default=None)

class Concordance(sqlobject.SQLObject):

    text = sqlobject.ForeignKey('WorkText')
    line = sqlobject.IntCol()
    char_index = sqlobject.IntCol()
