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
        c.options = [ (m.name, m.title) for m in model.Material.query.all() ]
        return render('anno/index.html')

    def annotate(self, id=None):
        c.error = ''
        c.content = ''
        c.server_api = self.server_api
        text = id if id else request.params.get('text', '')

        # TODO: warning in page (via javascript?) if not logged in
        # if not c.user:
        #    h.redirect_to(controller='user', action='login',
        #            came_from=request.url)

        if not text:
            c.error = 'No text to annotate!' 
        else:
            c.uri = text
            c.userid = c.user.id if c.user else c.author
            mat = model.Material.by_name(text)
            # get first resource that isn't pdf
            res = filter(lambda x: x.format != 'pdf', mat.resources)[0]
            c.content = genshi.HTML(render_resource(res))
        return render('anno/annotate.html')

