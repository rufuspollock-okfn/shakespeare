from StringIO import StringIO

from shakespeare.tests import *

class TestSiteController(TestController):

    def test_index(self):
        url = url_for(controller='site')
        res = self.app.get(url)
        print res
        assert "Home" in res

    def test_guide(self):
        url = url_for(controller='site', action='guide')
        res = self.app.get(url)
        assert 'guide to the features of the web interface' in res

    # 2008-04-26 rgrp: not working
    # seems to be issues inside the annotater stuff so leaving for the time
    # being.

#     def test_annotation(self):
#         url = url_for(controller='site', action='annotation')
#         res = self.app.get(url)
#         print str(res)
#         assert 'Annotations' in res
#  
#     def test_view_annotate(self):
#         url = url_for(action='view', name='sonnets_gut', format='annotate')
#         res = self.app.get(url)
#         assert 'Annotate' in res
#         print str(res)
#         assert 'THE SONNETS' in res
#         assert 'rest-annotate.js' in res
# 
#     def test_marginalia(self):
#         url = url_for(controller='site', action='marginalia', url='rest-annotate.js')
#         res = self.app.get(url)
#         print str(res)
#         assert 'AnnotationService' in res
# 
