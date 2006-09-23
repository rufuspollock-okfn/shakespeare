"""
Web interface to view and analyze shakespeare texts.
"""
import cherrypy
import os

import shakespeare.index
index = shakespeare.index.all
import shakespeare.utils
import shakespeare.format

import shakespeare.concordance

class ShakespeareWebInterface(object):

    def __init__(self):
        self.concordance = ConcordancePage()

    def index(self):
        try:
            import kid
            kid.enable_import(suffixes=[".html"])
            import shakespeare.template.index
            template = shakespeare.template.index.Template(works_index=index)
            result = str(template)
            # result = 'test'
            return result
        except Exception, inst:
            return '<p><strong>There was an error: ' +  str(inst) + '</strong></p>'
    index.exposed = True

    def view(self, name, format='plain'):
        text = shakespeare.dm.Material.byName(name)
        ff = file(text.cache_path)
        result = shakespeare.format.format_text(ff, format)
        ff.close()
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

