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
import shakespeare

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

    def _set_user(self):
        # do not bother with repoze.who stuff as unclear how exactly it works
        # identity = request.environ.get('repoze.who.identity', {})
        # c.username = identity.get('repoze.who.userid', '')
        c.username = request.environ.get('REMOTE_USER', '').decode('utf8')
        c.user = None
        if c.username:
            c.user = model.User.query.filter_by(openid=c.username).first()
        if not c.user and c.username:
            c.user = model.User(openid=c.username)
            model.Session.commit()
        c.remote_addr = request.environ.get('REMOTE_ADDR', 'Unknown IP Address')
        if c.remote_addr == 'localhost' or c.remote_addr == '127.0.0.1':
            # see if it was proxied
            c.remote_addr = request.environ.get('HTTP_X_FORWARDED_FOR',
                    '127.0.0.1')
        if c.user:
            c.author = c.user.name
        else:
            c.author = c.remote_addr
        c.author = unicode(c.author)

    def __before__(self, action, **params):
        c.site_title = config.get('site_title', 'Open Shakespeare')
        c.__version__ = shakespeare.__version__
        self._set_user()


