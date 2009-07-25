# utilities for migrate stuff
from migrate import *

# Based on http://www.luckydonkey.com/2008/07/27/sqlalchemy-migrate-upgrade-scripts-in-a-transaction/
# Unfortunately this does not seem to work!
# E.g. column drops still occur even when supposedly rolled-back ...
def wrap_in_transaction(f, *args, **kwargs):
    '''Decorator to wrap upgrade and downgrade commands in a transaction and rollback on failure.

    e.g.

    @wrap_in_transaction
    def upgrade():
        ...
    ''' 
    def wrapper(*args, **kwargs):
        connection = migrate_engine.connect()
        transaction = connection.begin()
        try:
            result = f(*args, **kwargs)
            transaction.commit()
            return result
        except:
            transaction.rollback()
            print 'Rolling back transaction'
            raise
        finally:
            connection.close()
    wrapper.__name__ = f.__name__
    wrapper.__dict__ = f.__dict__
    wrapper.__doc__ = f.__doc__
    return wrapper

