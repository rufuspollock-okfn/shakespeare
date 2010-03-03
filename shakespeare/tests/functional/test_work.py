from StringIO import StringIO

from shakespeare.tests import *
import shakespeare.model as model

class TestWorkController(TestController):
    @classmethod
    def setup_class(cls):
        cls.fixture = TestData.make_fixture()
    
    @classmethod
    def teardown_class(cls):
        TestData.remove_fixtures()
        model.Session.remove()

    def test_index(self):
        url = url_for(controller='work', action='index', id=None)
        res = self.app.get(url)
        assert 'Works - Index' in res, res
        assert 'Sonnet 18' in res, res
        # notes 
        assert '<h3>Some Notes' in res, res
        res = res.click('Sonnet 18')
        assert 'Info' in res, res

    def test_info(self):
        url = url_for(controller='work', action='info', id=TestData.name)
        res = self.app.get(url)
        assert 'Work - Info - ' in res
        assert 'Sonnet 18 (First Edition)' in res
        assert '<h3>Some Notes</h3>' in res, res
        # escape brackets for regex ...
        res = res.click('Sonnet 18 \(First Edition\)')
    
    def test_view(self):
        url = url_for(controller='work', action='index', id=None)
        res = self.app.get(url)
        res = res.click('View')
        assert self.fixture.title in res
    
    # annotate action tested in test_anno.py

