import logging

from shakespeare.lib.base import *

import shakespeare
import shakespeare.format
import shakespeare.model as model

# import this after dm so that db connection is set
# import annotater.store
# import annotater.marginalia

log = logging.getLogger(__name__)


class TextController(BaseController):

    def index(self):
        c.works_index = model.Material.query.all()
        return render('text/index.html')

    def info(self, id):
        name = id
        c.material = model.Material.by_name(name)
        if c.material:
            return render('text/info.html')
        else:
            abort(404)

    def view(self, id=''):
        name = id
        m = model.Material.by_name(name)
        if not m:
            abort(404)
        if m.resources:
            h.redirect_to(controller='resource', action='view',
                    id=m.resources[0].id)
        else:
            return 'No resource to view for this material'

