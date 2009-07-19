'''The application's domain model objects'''
import logging
import sqlalchemy
from sqlalchemy import orm

import meta
from dm import *

log = logging.getLogger(__name__)

def init_model(engine):
    '''Call me before using any of the tables or classes in the model'''
    meta.Session.configure(bind=engine)
    meta.engine = engine
    meta.metadata.bind = engine


class Repository(object):
    def __init__(self, ourmetadata, oursession):
        self.metadata = ourmetadata
        self.session = oursession

    def create_db(self):
        self.metadata.create_all(bind=self.metadata.bind)
        # sqlalchemy migrate hack
        from migrate.versioning.api import version_control, version 
        import shakespeare.migration.versions
        v = version(shakespeare.migration.__path__[0])
        log.info( "Setting current version to '%s'" % v )
        version_control(self.metadata.bind.url, shakespeare.migration.__path__[0], v) 

    def clean_db(self):
        self.metadata.drop_all(bind=self.metadata.bind)
        # remove migrate stuff if it exists
        import sqlalchemy.exceptions
        try:
            version_table = Table('migrate_version', self.metadata, autoload=True) 
            version_table.drop()
        except sqlalchemy.exceptions.NoSuchTableError:
            pass

    def rebuild_db(self):
        self.clean_db()
        self.create_db()

repo = Repository(metadata, Session)

