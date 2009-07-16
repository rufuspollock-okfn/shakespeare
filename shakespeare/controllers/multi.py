import logging

import genshi

from shakespeare.lib.base import *
import shakespeare
import shakespeare.format
import shakespeare.model as model

log = logging.getLogger(__name__)


class MultiController(BaseController):

    def index(self):
        names = [ m.name for m in model.Material.query.all() ]
        c.text_options = h.options_for_select(
                names
                )
        return render('multi/index.html')

    def view(self, id=None):
        format = request.params.get('format', 'plain')
        text1 = request.params.get('text_1', None)
        text2 = request.params.get('text_2', None)
        if not text1 or text2:
            c.error = 'Texts incorrectly specified'
            return render('multi/view.html')

        namelist = [ text1, text2 ]
        numtexts = len(namelist)
        textlist = [model.Material.by_name(tname) for tname in namelist]
        texthtml = {}
        for item in textlist:
            tfileobj = item.get_text()
            # hack for time being ...
            if item.format == 'mkd':
                ttext = h.markdown(tfileobj.read())
            else:
                ttext = shakespeare.format.format_text(tfileobj, format)
            texthtml[item.name] = genshi.HTML(ttext)
        c.frame_width = 100.0/numtexts - 4.0
        c.textlist = textlist
        c.texthtml = texthtml
        # set to not strip whitespace as o/w whitespace in pre tag gets removed
        return render('multi/view.html', strip_whitespace=False)

