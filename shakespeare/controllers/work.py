import logging

import genshi

from shakespeare.lib.base import *
import shakespeare.model as model
from shakespeare.controllers.our_resource import render_resource

log = logging.getLogger(__name__)


class WorkController(BaseController):

    def index(self):
        c.works_index = model.Work.query.all()
        return render('work/index.html')

    def info(self, id):
        name = id
        c.work = model.Work.by_name(name)
        if not c.work:
            abort(404)
        
        # TODO: stats link
        return render('work/info.html')

    def annotate(self, id=None):
        self.server_api = h.url_for(controller='anno_store', action='index')
        c.error = ''
        c.content = ''
        c.server_api = self.server_api
        work_name = id

        # TODO: warning in page (via javascript?) if not logged in
        # if not c.user:
        #    h.redirect_to(controller='user', action='login',
        #            came_from=request.url)

        if not work_name:
            c.error = 'No text to annotate!' 
        else:
            c.uri = work_name
            c.userid = c.user.id if c.user else c.author
            work = model.Work.by_name(work_name)
            # should be guaranteed not to be a pdf ...
            resource = work.default_resource
            c.content = genshi.HTML(render_resource(resource))
        return render('work/annotate.html')

    def view(self, id=None):
        from shakespeare.controllers.our_resource import OurResourceController
        resource_controller = OurResourceController()
        work = model.Work.by_name(id)
        if work is None:
            abort(404)
        resource = work.default_resource
        return resource_controller.view(resource.id)
    
