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

class WelcomePage:

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

    def concordance(self):
        import kid
        kid.enable_import(suffixes=[".html"])
        import shakespeare.template.concordance
        concordance = cc.concordance
        words = concordance.keys()
        words.sort()
        template = shakespeare.template.concordance.Template(words=words, stats=cc.stats)
        result = template.serialize()
        # result = str(cc)
        return result
    concordance.exposed = True
  

cherrypy.root = WelcomePage()

if __name__ == '__main__':
    cherrypy.lowercase_api = True
    # cherrypy.config.update(file = 'tutorial.conf')
    cherrypy.config.update({'server.showTracebacks' : True })
    cherrypy.server.start()
    
"""    
[global]
server.socketPort = 8080
server.threadPool = 10
server.environment = "production"
# server.showTracebacks = True
# server.logToScreen = False
"""
