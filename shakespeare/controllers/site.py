import logging

import genshi

from shakespeare.lib.base import *

import shakespeare
import shakespeare.index
import shakespeare.format
import shakespeare.concordance
import shakespeare.model as model

# import this after dm so that db connection is set
import annotater.store
import annotater.marginalia

log = logging.getLogger(__name__)


class SiteController(BaseController):

    def index(self):
        c.works_index = shakespeare.index.all
        return render('index')

    def guide(self):
        return render('guide')

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
            tpath = textlist[0].get_cache_path('plain')
            result = file(tpath).read()
            status = '200 OK'
            response.headers['Content-Type'] = 'text/plain'
            return result
        texts = []
        for item in textlist:
            tpath = item.get_cache_path('plain')
            tfileobj = file(tpath)
            ttext = shakespeare.format.format_text(tfileobj, format)
            thtml = genshi.XML(ttext)
            texts.append(thtml)
        # would have assumed this would be 100.0/numtexts but for some reason
        # you need to allow more room (maybe because of the scrollbars?)
        # result is not consistent across browsers ...
        c.frame_width = 100.0/numtexts - 4.0
        c.texts = texts
        # set to not strip whitespace as o/w whitespace in pre tag gets removed
        return render('view', strip_whitespace=False)

    def concordance(self, word=None):
        # TODO: support concordance/word
        return self.concordance_index()

    def concordance_index(self):
        stats = shakespeare.concordance.Statistics()
        c.words = stats.keys()
        return render('concordance')

    def concordance_word(self, word=None):
        # TODO: sort by work etc
        import shakespeare.textutils
        refs = []
        cc = shakespeare.concordance.Concordance()
        if word is not None:
            refs = list(cc.get(word))
        newrefs = []
        for ref in refs:
            # we use the 'plain' format when building the concordance
            tpath = ref.text.get_cache_path('plain')
            ff = file(tpath)
            snippet = shakespeare.textutils.get_snippet(ff, ref.char_index)
            ref.snippet = snippet
        c.word = word
        c.refs = refs
        return render('concordance_by_word')

    # 2008-04-26 (rgrp): none of these annotater related items
    # seem to working properly
    # think it is related to annotater so leaving this alone for time being

    def marginalia(self):
        prefix = '/' + h.url_for('marginalia')
        media_app = annotater.marginalia.MarginaliaMedia(prefix)
        out = media_app(request.environ, self.start_response)
        return out

    def annotation(self):
        store = annotater.store.AnnotaterStore()
        return store(request.environ, self.start_response)

    def view_annotate(self):
        # only one name here ...
        name = request.params.get('name')
        textobj = model.Material.byName(name)
        tpath = textobj.get_cache_path('plain')
        tfileobj = file(tpath)
        formatter = shakespeare.format.TextFormatterAnnotate()
        # not perfect in that we might have the application mounted somewhere
        annotation_store_fqdn = wsgiref.util.application_uri(request.environ)
        page_url = wsgiref.util.request_uri(request.environ)
        ttext = formatter.format(tfileobj, page_uri=page_url)
        thtml = genshi.HTML(ttext)

        prefix = cfg.get('annotater', 'marginalia_prefix')
        marginalia_media = annotater.marginalia.get_media_header(prefix,
                annotation_store_fqdn,
                page_url)
        buttons = annotater.marginalia.get_buttons(page_url)
        marginalia_media = genshi.HTML(marginalia_media)
        buttons = genshi.HTML(buttons)

        c.text_with_annotation=thtml
        c.marginalia_media=marginalia_media
        c.annotation_buttons=buttons
        return render('view_annotate', strip_whitespace=False)

