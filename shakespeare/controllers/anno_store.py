import logging

from annotator.store import AnnotatorStore

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

store = AnnotatorStore('anno_store')
def AnnoStoreController(environ, start_response):
    return store(environ, start_response)

