from shakespeare.tests import *

import shakespeare.model as model
import shakespeare.tests.test_stats


class TestSearchController(TestController):

    text = make_fixture()
    text2 = make_fixture2()

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

    def test_text_stats_index(self):
        url = url_for(controller='stats', action='text', id=None)
        res = self.app.get(url)
        assert self.text.name in res
        assert self.text2.name in res
    
    def test_text_stats(self):
        url = url_for(controller='stats', action='text', id=self.text.name)
        res = self.app.get(url)
        assert 'summer' in res

    # TODO: stats for a text with no associated items 
    def test_text_no_stats(self):
        url = url_for(controller='stats', action='text', id=self.text2.name)
        res = self.app.get(url)
        assert 'Sorry, no statistics' in res

    def test_word_stats(self):
        shakespeare.tests.test_stats.stats_fixture(self.text2)
        word = 'summer'
        url = url_for(controller='stats', action='word', id=word)
        res = self.app.get(url)
        assert 'summer' in res
        assert self.text.title in res
        assert self.text2.title in res
        assert '3' in res

