"""The application's Globals object"""
from pylons import config

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.annotator_store = config.get('literature.annotator.store', '')
        self.annotator_consumer_key = config.get('literature.annotator.consumer_key', '')
        self.annotator_consumer_secret = config.get('literature.annotator.consumer_secret', '')
        self.deliverance_enabled = bool(config.get('deliverance.enabled', ''))

