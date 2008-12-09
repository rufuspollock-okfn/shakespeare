import logging

import genshi

from shakespeare.lib.base import *

import shakespeare.model as model

log = logging.getLogger(__name__)


class WorkController(BaseController):

    def index(self):
        c.works_index = model.Work.query.all()
        return render('work/index.html')

    def info(self, id):
        name = id
        c.work = model.Work.by_name(name)
        if c.work:
            return render('work/info.html')
        else:
            abort(404)

