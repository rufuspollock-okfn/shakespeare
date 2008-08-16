from shakespeare.tests import *

import shakespeare.model as model
import shakespeare.tests.test_stats


class TestSearchController(TestController):

    text = make_fixture()

    def setUp(self):
        model.Session.begin()
        shakespeare.tests.test_stats.stats_fixture(self.text)

    def tearDown(self):
        model.Session.rollback()
        model.Session.remove()

    def test_index(self):
        url = url_for(controller='stats')
        res = self.app.get(url)
        assert 'Stats' in res
    
    def test_stats(self):
        text = make_fixture()
        url = url_for(controller='stats', action='text', id=self.text.name)
        res = self.app.get(url)
        assert 'summer' in res

