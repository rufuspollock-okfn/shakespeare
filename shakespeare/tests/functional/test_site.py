from StringIO import StringIO

from shakespeare.tests import *

class TestSiteController(TestController):

    def test_index(self):
        url = url_for(controller='site')
        res = self.app.get(url)
        print res
        assert 'Index of Shakespeare plays' in res
        assert 'The Tempest' in res

    def test_view_1(self):
        url = url_for(controller='site', action='view', name='tempest_gut',
            format='plain')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_index_2(self):
        url = url_for(controller='site')
        res = self.app.get(url)
        res = res.click('The Tempest', index=0)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_2(self):
        url = url_for(controller='site', action='view',
                name=['tempest_gut','tempest_gut_f'], format='plain')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_3(self):
        url = url_for(controller='site', action='view',
                name=['tempest_gut', 'tempest_gut_f'], format='raw')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_with_unicode_source(self):
        url = url_for(controller='site', action='view',
                name='all_is_well_that_ends_well_gut_f', format='plain')
        res = self.app.get(url)
        assert "All's Well, that Ends Well" in res

    def test_guide(self):
        url = url_for(controller='site', action='guide')
        res = self.app.get(url)
        assert 'guide to the features of the Open Shakespeare web' in res

    def test_concordance(self):
        url = url_for(controller='site', action='concordance')
        res = self.app.get(url)

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
