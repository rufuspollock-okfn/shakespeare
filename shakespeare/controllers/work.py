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
        h.redirect_to(controller='work', action='view', id=id)

    def view(self, id=None):
        c.work = model.Work.by_name(id)
        if c.work is None:
            abort(404)

        c.annotator_enabled = True
        # should be guaranteed not to be a pdf ...
        resource = c.work.default_resource
        c.content = genshi.HTML(render_resource(resource))
        return render('work/view.html')
