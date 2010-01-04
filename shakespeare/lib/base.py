"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.i18n import _, ungettext, N_

from pylons.controllers import WSGIController
from pylons.templating import render_genshi as render
from pylons import config

import shakespeare.lib.helpers as h
import shakespeare.model as model

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            model.Session.remove()

    def __before__(self, action, **params):
        c.site_title = config.get('site_title', 'Open Shakespeare')

