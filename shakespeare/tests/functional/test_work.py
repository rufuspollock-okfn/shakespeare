from StringIO import StringIO

from shakespeare.tests import *
import shakespeare.model as model

class TestWorkController(TestController):
    def setUp(cls):
        TestData.make_fixture()
    
    def tearDown(cls):
        TestData.remove_fixtures()
        model.Session.remove()

    def test_index(self):
        url = url_for(controller='work', action='index', id=None)
        res = self.app.get(url)
        print res
        assert 'Works - Index' in res

    def test_info(self):
        url = url_for(controller='work', action='info', id=TestData.name)
        res = self.app.get(url)
        assert 'Work - Info - ' in res
        assert 'Sonnet 18 (First Edition)' in res
        assert '<h3>Some Notes</h3>' in res, res
        # escape brackets for regex ...
        res = res.click('Sonnet 18 \(First Edition\)')
        
