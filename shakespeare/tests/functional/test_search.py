import StringIO

from shakespeare.tests import *

import shakespeare.search

class TestSearchController(TestController):

    @classmethod
    def setup_class(self):
        self.text = make_fixture()
        self.sindex = shakespeare.search.SearchIndex.default_index()
        self.sindex.add_item(StringIO.StringIO(self.text.content), self.text.name)

    @classmethod
    def teardown_class(self):
        self.sindex.remove_item(self.text.name)

    def test_index(self):
        url = url_for(controller='search')
        res = self.app.get(url)
        assert "Search" in res
    
    def test_search(self):
        url = url_for(controller='search')
        res = self.app.get(url)
        form = res.forms[0]
        form['query'] = 'summer'
        res = form.submit()
        assert 'There were 2 results' in res
        assert 'Search Results' in res
        assert 'Sonnet 18' in res
        assert 'Shall I compare thee' in res

