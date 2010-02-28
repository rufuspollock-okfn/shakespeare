import logging

import genshi
import annotator.middleware

from shakespeare.lib.base import *
from shakespeare.controllers.our_resource import render_resource

log = logging.getLogger(__name__)

class AnnoController(BaseController):
    media_mount_path = '/jsannotate'
    server_api = h.url_for(controller='anno_store')
    anno_middleware = annotator.middleware.JsAnnotateMiddleware(None,
            media_mount_path, server_api)

    def index(self):
        c.works = model.Work.query()
        return render('anno/index.html')

    def annotate(self, id=None):
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
        return render('anno/annotate.html')

