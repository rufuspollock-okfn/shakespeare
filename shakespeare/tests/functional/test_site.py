from StringIO import StringIO

from shakespeare.tests import *

class TestSiteController(TestController):
    def test_index(self):
        url = url_for(controller='site', action='index')
        res = self.app.get(url)
        print res
        assert "Home" in res

    def test_word_of_the_day(self):
        url = url_for(controller='site', action='index')
        res = self.app.get(url)
        # css id
        assert 'word-of-the-day' in res
        assert 'No words yet!' in res

