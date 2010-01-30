import logging
import os

import genshi
from pylons import config

from shakespeare.lib.base import *

import shakespeare
import shakespeare.format
import shakespeare.model as model

# import this after dm so that db connection is set
# import annotater.store
# import annotater.marginalia

log = logging.getLogger(__name__)

DELIVERANCE_ENABLE = bool(config.get('deliverance.enable', ''))


# based on http://rufuspollock.org/code/deliverance
import paste.urlmap
import deliverance.middleware
import paste.proxy
from webob import Request, Response
from deliverance.middleware import DeliveranceMiddleware, SubrequestRuleGetter
from deliverance.log import PrintingLogger
def create_deliverance_proxy():
    # where we are proxying from
    dest = config['deliverance.dest']

    # use a urlmap so we can mount theme and urlset
    app = paste.urlmap.URLMap()

    # set up theme consistent with our rules file
    app['/theme.html'] = Response(render('index.html'))

    # rules_path = os.path.join('demo-rules.xml')
    # rules = open(rules_path).read()
    rules = '''<ruleset>

  <theme href="/theme.html" />

  <!-- These are the default rules for anything with class="default" or no class: -->
  <rule>
    <replace content="children:#content" theme="children:#content" />
    <append content="children:#sidebar" theme="children:#primary" />
  </rule>
</ruleset>
'''
    app['/rules.xml'] = Response(rules, content_type="application/xml")

    class MyProxy(object):
        def __init__(self, dest):
           self.proxy = paste.proxy.Proxy(dest) 
        
        def __call__(self, environ, start_response):
            req = Request(environ)
            res = req.get_response(self.proxy)
            # result = ''
            # for out in self.proxy(environ, start_response):
            #    result += out
            # res = Response(result)
            res.decode_content()
            return res(environ, start_response)

    app['/'] = MyProxy(dest)

    deliv = DeliveranceMiddleware(app, SubrequestRuleGetter('/rules.xml'),
        PrintingLogger,
        log_factory_kw=dict(print_level=logging.WARNING))
    return deliv


class SiteController(BaseController):
    def index(self):
        return render('index.html')

    def about(self):
        if DELIVERANCE_ENABLE:
            return self.deliverance(request.environ, self.start_response)
        else:
            return render('about.html')

    def guide(self):
        return render('guide.html')

    def news(self):
        if DELIVERANCE_ENABLE:
            # modify path for proxy to strip out /news/
            currentpath = request.environ['PATH_INFO']
            request.environ['PATH_INFO'] = currentpath[5:]
            return self.deliverance(request.environ, self.start_response)
        else:
            return ''

    @property
    def deliverance(self):
        if not hasattr(self, '_deliverance'):
            self._deliverance = create_deliverance_proxy()
        return self._deliverance

