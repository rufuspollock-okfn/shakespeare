"""
Web interface to view and analyze shakespeare texts.
"""
import os

import cherrypy
import genshi.template

import shakespeare.index
import shakespeare.format
import shakespeare.concordance
import shakespeare.dm

import shakespeare

cfg = shakespeare.conf()
template_path = cfg.get('web', 'template_dir')
template_loader = genshi.template.TemplateLoader([template_path],
        auto_reload=True)

class ShakespeareWebInterface(object):

    def __init__(self):
        self.concordance = ConcordancePage()

    def index(self):
        try:
            index = shakespeare.index.all
            tmpl = template_loader.load('index.html')
            result = tmpl.generate(works_index=index).render()
            return result
        except Exception, inst:
            return '<p><strong>There was an error: ' +  str(inst) + '</strong></p>'
    index.exposed = True

    def guide(self):
        template = template_loader.load('guide.html')
        result = template.generate().render()
        return result
    guide.exposed = True

    def view(self, name, format='plain'):
        import shakespeare.dm
        namelist = name.split()
        numtexts = len(namelist)
        textlist = [shakespeare.dm.Material.byName(tname) for tname in namelist]
        # special case (only return the first text)
        if format == 'raw':
            cherrypy.response.headers["Content-Type"] = "text/plain"
            tpath = textlist[0].get_cache_path('plain')
            return file(tpath).read()
        texts = []
        for item in textlist:
            tpath = item.get_cache_path('plain')
            tfileobj = file(tpath)
            ttext = shakespeare.format.format_text(tfileobj, format)
            import genshi.input
            import StringIO
            thtml = genshi.input.HTMLParser(StringIO.StringIO(ttext))
            texts.append(thtml)
        # would have assumed this would be 100.0/numtexts but for some reason
        # you need to allow more room (maybe because of the scrollbars?)
        # result is not consistent across browsers ...
        frame_width = 100.0/numtexts - 4.0
        template = template_loader.load('view.html')
        result = template.generate(frame_width=frame_width, texts=texts)
        return result.render()

    view.exposed = True

class ConcordancePage(object):

    def index(self):
        stats = shakespeare.concordance.Statistics()
        words = stats.keys()
        template = template_loader.load('concordance.html')
        result = template.generate(words=words)
        return result.render()
    index.exposed = True

    def word(self, word=None):
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
        template = template_loader.load('concordance_by_word.html')
        result = template.generate(word=word, refs=refs) 
        return result.render()
    word.exposed = True

