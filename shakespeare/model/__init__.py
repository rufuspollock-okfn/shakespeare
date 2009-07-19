'''The application's domain model objects'''
import sqlalchemy
from sqlalchemy import orm

import meta
from dm import *

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

    def clean_db(self):
        self.metadata.drop_all(bind=self.metadata.bind)

    def rebuild_db(self):
        self.clean_db()
        self.create_db()

repo = Repository(metadata, Session)

