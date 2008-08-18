import logging

import pygooglechart

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
        # 40 seems limit for google
        data = [ (s.word, s.freq) for s in c.stats[:40] ]
        c.img_url = self.vertical_bar_chart(data)
        return render('stats/text')

    # TODO: factor this out to its module (?)
    def vertical_bar_chart(self, data, width=500):
        # tranpose
        tdata = zip(*data)
        labels = list(tdata[0])
        values = tdata[1]
        bar_width = 10
        # add 5 for space between bars
        height = (bar_width + 5) * len(values)
        # was setting x_range but automatic behaviour seems better
        # x_range = (min(values), max(values))
        chart = pygooglechart.StackedHorizontalBarChart(width, height)
        chart.set_bar_width(bar_width)
        chart.set_colours(['cc0033'])
        chart.add_data(values)
        # have to reverse the labels for vertical
        labels.reverse()
        chart.set_axis_labels(pygooglechart.Axis.LEFT, labels)
        chart.set_axis_range(pygooglechart.Axis.BOTTOM, 0, max(values))
        chart.set_axis_range(pygooglechart.Axis.TOP, 0, max(values))
        url = chart.get_url()
        return url

