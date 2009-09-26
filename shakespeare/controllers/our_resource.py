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
        return render('text/view.html', strip_whitespace=False)

import shakespeare.format
def render_resource(res):
    tfileobj = res.get_stream()
    if res.format == 'mkd':
        ttext = h.markdown(tfileobj.read())
    elif res.format == 'txt':
        ttext = shakespeare.format.format_text(tfileobj, 'lineno')
    elif res.format == 'pdf':
        # can't render pdfs!
        ttext = '<a href="%s">Link to PDF</a>' % h.url_for('pdf', url=res.material.name+'.pdf')
    elif res.format == 'html':
        ttext = tfileobj.read()
    else:
        raise Exception('Unknown resource format')
    return ttext

