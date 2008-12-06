import logging

import genshi

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
        # first check ?name param then do name in url
        name = request.params.get('name', '')
        if not name:
            name = id
        if not name:
            abort(404)
        format = request.params.get('format', 'plain')
        namelist = name.split()
        numtexts = len(namelist)
        textlist = [model.Material.byName(tname) for tname in namelist]
        # special case (only return the first text)
        if format == 'raw':
            result = textlist[0].get_text().read()
            status = '200 OK'
            response.headers['Content-Type'] = 'text/plain'
            return result
        texthtml = {}
        for item in textlist:
            tfileobj = item.get_text()
            ttext = shakespeare.format.format_text(tfileobj, format)
            texthtml[item.name] = genshi.HTML(ttext)
        # would have assumed this would be 100.0/numtexts but for some reason
        # you need to allow more room (maybe because of the scrollbars?)
        # result is not consistent across browsers ...
        c.frame_width = 100.0/numtexts - 4.0
        c.textlist = textlist
        c.texthtml = texthtml
        # set to not strip whitespace as o/w whitespace in pre tag gets removed
        return render('text/view.html', strip_whitespace=False)

