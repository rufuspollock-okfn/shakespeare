"""
Web interface to view and analyze shakespeare texts.
"""
import cherrypy
import os

import shakespeare.work
index = shakespeare.work.index.all 
from shakespeare.utils import get_local_path
import shakespeare.format

import shakespeare.concordancer
cc = shakespeare.concordancer.get_concordancer()

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

    def view(self, text_url=None, version='cleaned', format='plain'):
        localPath = get_local_path(text_url, version)
        ff = file(localPath)
        if format == 'plain':
            result = '<pre>' + ff.read() + '</pre>'
        else:
            formatter = shakespeare.format.TextFormatter(ff)
            result = formatter.format(format)
            # import kid
            # kid.enable_import(suffixes=['.html'])
            # module = __import__('shakespeare.template.format_' + format, '', '', '*')
            # template = module.Template(fileobj=ff)
            # result = template.serialize()
        ff.close()
        return result
    view.exposed = True

class ConcordancePage(object):

    def index(self):
        import kid
        kid.enable_import(suffixes=[".html"])
        import shakespeare.template.concordance
        concordance = cc.concordance
        words = concordance.keys()
        words.sort()
        template = shakespeare.template.concordance.Template(words=words,
                concordance=concordance, stats=cc.stats)
        result = template.serialize()
        # result = str(cc)
        return result
    index.exposed = True

    def word(self, word=None):
        # TODO: sort by work etc
        import shakespeare.textutils
        refs = []
        if word is not None:
            refs = cc.concordance[word]
        newrefs = []
        for ref in refs:
            snippet = shakespeare.textutils.get_snippet(ref[0], ref[2])
            newref = list(ref)
            newref.append(snippet)
            newrefs.append(newref)
        import kid
        kid.enable_import(suffixes=[".html"])
        import shakespeare.template.concordance_by_word
        template = shakespeare.template.concordance_by_word.Template(word=word,
               refs=newrefs) 
        result = template.serialize()
        return result
    word.exposed = True

