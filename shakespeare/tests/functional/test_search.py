import StringIO

from shakespeare.tests import *

import shakespeare.search

class TestSearchController(TestController):

    def setUp(self):
        # TODO: remove this item from index in tearDown
        text = make_fixture()
        sindex = shakespeare.search.SearchIndex.default_index()
        sindex.add_item(StringIO.StringIO(text.content))

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
        assert 'Search Results' in res
        assert 'Shall I compare thee' in res

