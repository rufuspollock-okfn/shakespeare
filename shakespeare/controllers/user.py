import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)


class UserController(BaseController):

    def index(self):
        if not c.user:
            h.redirect_to(controller='user', action='login', id=None)
        else:
            h.redirect_to(controller='user', action='read', id=c.user.id)

    def read(self, id=None):
        if id:            
            c.read_user = model.User.query.get(id)
        if not c.read_user:
            abort(404)
        c.is_myself = c.read_user.id == c.user.id
        return render('user/read.html')

    def login(self):
        if not c.user:
            form = render('user/openid_form.html')
            # /login_openid page need not exist -- request gets intercepted by openid plugin
            form = form.replace('FORM_ACTION', '/login_openid')
            return form
        else:
            came_from = request.params.get('came_from', None)
            if came_from:
                h.redirect_to(str(came_from))
            else:
                h.redirect_to(controller='user', action='read', id=c.user.id)

    def logout(self):
        c.user = None
        return render('user/logout.html')

