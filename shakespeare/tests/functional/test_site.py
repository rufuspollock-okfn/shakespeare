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
    
    def test_word_of_the_day(self):
        url = url_for(controller='site')
        res = self.app.get(url)
        # css id
        assert 'word-of-the-day' in res
        assert 'No words yet!' in res

