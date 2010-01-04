import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

class AnthologyController(BaseController):

    def index(self):
        c.works_index = model.Work.query.all()
        return render('anthology/index.html')

    def edit(self, id=None):
        text_names = request.params.getall('text')
        c.selected_items = []
        for name in text_names:
            item = model.Work.by_name(name)
            c.selected_items.append(item)
        return render('anthology/edit.html')
        
