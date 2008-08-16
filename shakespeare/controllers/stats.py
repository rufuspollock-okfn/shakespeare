import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

import shakespeare.stats

class StatsController(BaseController):

    def index(self):
        return render('stats/index')
    
    def text(self, id):
        text_name = id
        text = model.Material.byName(text_name)
        stats = shakespeare.stats.Stats()
        c.text = text
        c.stats = stats.text_stats(text)
        return render('stats/text')

