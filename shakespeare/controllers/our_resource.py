import logging

import genshi

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

class OurResourceController(BaseController):

    def index(self):
        return 'Resource'

    def view(self, id):
        res = model.Resource.query.get(id)
        if not res:
            abort(404)
        if res.material:
            c.title = res.material.title
        else:
            c.title = ''
        c.texthtml = genshi.HTML(render_resource(res))
        # strip_whitespace does not work with pylons 0.9.7
        return render('text/view.html')

import os
import shakespeare.format
def render_resource(res):
    if res.format == 'mkd':
        tfileobj = res.get_stream()
        ttext = h.markdown(tfileobj.read())
    elif res.format == 'txt':
        tfileobj = res.get_stream()
        ttext = shakespeare.format.format_text(tfileobj, 'lineno')
    elif res.format == 'pdf':
        # can't render pdfs!
        # TODO: should probably use name but pdf generation goes on original
        # name
        # ttext = '<a href="%s">Link to PDF</a>' % h.url_for('pdf', url=res.material.name+'.pdf')
        ttext = '<a href="%s">Link to PDF</a>' % h.url_for('pdf',
                url=os.path.basename(res.locator))
    elif res.format == 'html':
        tfileobj = res.get_stream()
        ttext = tfileobj.read()
    else:
        raise Exception('Unknown resource format')
    return ttext

