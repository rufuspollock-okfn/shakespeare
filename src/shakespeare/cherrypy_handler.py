"""
Tutorial - Passing variables

This tutorial shows you how to pass GET/POST variables to methods.
"""
import cherrypy
import os

from shakespeare.download import make_index
index = make_index() 
from shakespeare.utils import get_local_path
import shakespeare.format

import shakespeare.concordancer
concordancer = shakespeare.concordancer.get_concordancer()

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

#    def concordance(self):
#        import kid
#        kid.enable_import(suffixes=[".html"])
#        import shakespeare.template.concordance
#        template = shakespeare.template.concordance.Template(concordancer=concordancer)
#        result = template.serialize()
#        return result
#    concordance.exposed = True
  

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
