'''The application's domain model objects'''
import sqlalchemy
from sqlalchemy import orm

import meta
from dm import *

def init_model(engine):
    '''Call me before using any of the tables or classes in the model'''
    meta.Session.configure(bind=engine)
    meta.engine = engine

