from shakespeare.tests import *

class TestSearchController(TestController):

    def test_index(self):
        url = url_for(controller='search')
        res = self.app.get(url)
        assert "Search" in res
    
    def test_search(self):
        url = url_for(controller='search')
        res = self.app.get(url)
        form = res.forms[0]
        # for this to work need to have added phoenix to the index
        # TODO: put this in setUp or something ...
        form['query'] = 'Phoenix'
        res = form.submit()
        assert 'Search Results' in res
        assert 'Phoenix' in res

