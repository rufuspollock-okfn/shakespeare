import logging

import genshi

from shakespeare.lib.base import *
import shakespeare
import shakespeare.format
import shakespeare.model as model

log = logging.getLogger(__name__)


class MultiController(BaseController):

    def index(self):
        c.options = [ (m.name, m.title) for m in model.Material.query.all() ]
        return render('multi/index.html')

    def view(self, id=None):
        format = request.params.get('format', 'plain')
        text1 = request.params.get('text_1', None)
        text2 = request.params.get('text_2', None)
        if not text1 or not text2:
            c.error = 'Texts incorrectly specified'
            return render('multi/view.html')

        namelist = [ text1, text2 ]
        numtexts = len(namelist)
        textlist = [model.Material.by_name(tname) for tname in namelist]
        texthtml = {}
        for item in textlist:
            tfileobj = item.get_text()
            # TODO: check format
            ttext = shakespeare.format.format_text(tfileobj, format)
            texthtml[item.name] = genshi.HTML(ttext)
        c.frame_width = 100.0/numtexts - 4.0
        c.textlist = textlist
        c.texthtml = texthtml
        # set to not strip whitespace as o/w whitespace in pre tag gets removed
        # strip_whitespace does not work with pylons 0.9.7
        # return render('multi/view.html', strip_whitespace=False)
        return render('multi/view.html')

