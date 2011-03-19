import logging

import paste.proxy
from pylons import config

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

class AnnostoreController(BaseController):
    def view(self, url):
        '''Proxy to a remote annotation store (solves cross-domain scripting
        issues).
        '''
        proxy_site = config['literature.annotator.store']
        request.environ['PATH_INFO'] = url
        proxy = paste.proxy.Proxy(proxy_site) 
        return proxy(request.environ, self.start_response)

