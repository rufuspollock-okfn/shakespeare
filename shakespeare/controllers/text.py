import logging

import genshi

from shakespeare.lib.base import *

import shakespeare
import shakespeare.index
import shakespeare.format
import shakespeare.concordance
import shakespeare.model as model

# import this after dm so that db connection is set
# import annotater.store
# import annotater.marginalia

log = logging.getLogger(__name__)


class TextController(BaseController):

    def index(self):
        c.works_index = shakespeare.index.all
        return render('text/index')

    def view(self):
        name = request.params.get('name', '')
        format = request.params.get('format', 'plain')
        if format == 'annotate':
            return self.view_annotate(name)
        namelist = name.split()
        numtexts = len(namelist)
        textlist = [model.Material.byName(tname) for tname in namelist]
        # special case (only return the first text)
        if format == 'raw':
            result = textlist[0].get_text().read()
            status = '200 OK'
            response.headers['Content-Type'] = 'text/plain'
            return result
        texts = []
        for item in textlist:
            tfileobj = item.get_text()
            ttext = shakespeare.format.format_text(tfileobj, format)
            thtml = genshi.HTML(ttext)
            texts.append(thtml)
        # would have assumed this would be 100.0/numtexts but for some reason
        # you need to allow more room (maybe because of the scrollbars?)
        # result is not consistent across browsers ...
        c.frame_width = 100.0/numtexts - 4.0
        c.texts = texts
        # set to not strip whitespace as o/w whitespace in pre tag gets removed
        return render('text/view', strip_whitespace=False)

