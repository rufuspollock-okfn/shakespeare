import logging

import genshi
import annotator.middleware

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

class AnnoController(BaseController):
    media_mount_path = '/jsannotate'
    server_api = h.url_for(controller='anno_store')
    anno_middleware = annotator.middleware.JsAnnotateMiddleware(None,
            media_mount_path, server_api)

    def index(self):
        c.options = [ (m.name, m.title) for m in model.Material.query.all() ]
        return render('anno/index.html')

    def annotate(self, id=None):
        c.server_api = self.server_api
        if id:
            text = id
        else:
            text = request.params.get('text', '')
        c.error = ''
        if not text:
            c.error = 'No text to annotate!' 
            c.content = ''
        else:
            mat = model.Material.by_name(text)
            content = mat.get_text().read()
            # HACK: limit size for present
            content = content[:500]
            c.content = genshi.HTML('<pre>%s</pre>' % content)
        out = render('anno/annotate.html')
        # out is a webhelpers.html.builder.literal
        # we want to work with raw html ...
        # out = unicode(out)
        # out = self.anno_middleware.modify_html(out, include_jquery=False)
        return out

