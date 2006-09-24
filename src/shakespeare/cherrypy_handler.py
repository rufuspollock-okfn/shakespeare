"""
Web interface to view and analyze shakespeare texts.
"""
import cherrypy
import os

import shakespeare.index
import shakespeare.utils
import shakespeare.format
import shakespeare.concordance
import shakespeare.dm

class ShakespeareWebInterface(object):

    def __init__(self):
        self.concordance = ConcordancePage()

    def index(self):
        try:
            import kid
            kid.enable_import(suffixes=[".html"])
            import shakespeare.template.index
            index = shakespeare.index.all
            template = shakespeare.template.index.Template(works_index=index)
            result = str(template)
            return result
        except Exception, inst:
            return '<p><strong>There was an error: ' +  str(inst) + '</strong></p>'
    index.exposed = True

    def view(self, name, format='plain'):
        import shakespeare.dm
        namelist = name.split()
        numtexts = len(namelist)
        textlist = [shakespeare.dm.Material.byName(tname) for tname in namelist]
        # special case (only return the first text)
        if format == 'raw':
            cherrypy.response.headers["Content-Type"] = "text/plain"
            return file(textlist[0].cache_path).read()
        texts = [ shakespeare.format.format_text(file(text.cache_path), format)
            for text in textlist ]
        # would have assumed this would be 100.0/numtexts but for some reason
        # you need to allow more room (maybe because of the scrollbars?)
        # result is not consistent across browsers ...
        frame_width = 100.0/numtexts - 4.0
        import kid
        kid.enable_import(suffixes=['.html'])
        import shakespeare.template.view
        template = shakespeare.template.view.Template(frame_width=frame_width,
                texts=texts)
        result = template.serialize()
        return result

    view.exposed = True

class ConcordancePage(object):

    def index(self):
        import kid
        kid.enable_import(suffixes=[".html"])
        import shakespeare.template.concordance
        cc = shakespeare.concordance.Concordance()
        stats = shakespeare.concordance.Statistics()
        words = cc.keys()
        # already sorted
        # words.sort()
        template = shakespeare.template.concordance.Template(words=words,
               stats=stats)
        result = template.serialize()
        # result = str(cc)
        return result
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
            ff = file(ref.text.cache_path)
            snippet = shakespeare.textutils.get_snippet(ff, ref.char_index)
            ref.snippet = snippet
        import kid
        kid.enable_import(suffixes=[".html"])
        import shakespeare.template.concordance_by_word
        template = shakespeare.template.concordance_by_word.Template(word=word,
               refs=refs) 
        result = template.serialize()
        return result
    word.exposed = True

