import logging

import pygooglechart

from shakespeare.lib.base import *
log = logging.getLogger(__name__)
import shakespeare.stats

class StatsController(BaseController):

    def index(self):
        return render('stats/index.html')

    def text_index(self):
        # only get those texts with stats
        c.texts = model.Material.query.all()
        import shakespeare.controllers.text
        ctrl = shakespeare.controllers.text.TextController()
        return ctrl.index()

    def text(self, id=None):
        text_name = id
        text = model.Material.by_name(text_name)
        # no id or no text by that id
        if not text:
            return self.text_index()
        stats = shakespeare.stats.Stats()
        c.text = text
        c.stats = stats.text_stats(text)
        # 40 seems limit for google
        data = [ (s.word, s.freq) for s in c.stats[:40] ]
        try:
            c.img_url = self.vertical_bar_chart(data)
        except:
            # TODO: log error message
            c.img_url = ''
        return render('stats/text.html')

    def word_index(self):
        import sqlalchemy.sql as sql
        st = model.statistic_table
        q = sql.select([st.c.word], distinct=True)
        c.words = [ w[0] for w in q.execute().fetchall() ]
        return render('stats/word_index.html')
    
    def word(self, id):
        if id is None:
            return self.word_index()
        word = id
        c.word = word
        stats = shakespeare.stats.Stats()
        c.stats = stats.word_stats(word)
        # will not have that many texts so do not need to limit c.stats
        data = [ (s.text.title[:min(len(s.text.title), 10)], s.freq) for s in c.stats ]
        try:
            c.img_url = self.vertical_bar_chart(data)
        except:
            # TODO: log error message
            c.img_url = ''
        return render('stats/word.html')

    # TODO: factor this out to its module (?)
    def vertical_bar_chart(self, data, width=300):
        if not data:
            return ''
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

