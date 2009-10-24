from StringIO import StringIO

from shakespeare.tests import *
import shakespeare.model as model

class TestTextController(TestController):
    @classmethod
    def setup_class(self):
        self.text = TestData.make_fixture()

    @classmethod
    def teardown_class(self):
        TestData.remove_fixtures()

    def test_index(self):
        url = url_for(controller='text', action='index', id=None)
        res = self.app.get(url)
        print res
        assert 'Texts - Index' in res
        assert 'Sonnet 18' in res

    def test_info(self):
        url = url_for(controller='text', action='info', id='test_sonnet18')
        res = self.app.get(url)
        assert 'Sonnet 18' in res, res

    def test_view_1(self):
        url = url_for(controller='text', action='view', id='test_sonnet18',
            format='plain')
        res = self.app.get(url)
        res = res.follow()
        assert 'Shall I compare thee' in res, str(res)[:5000]

    def test_index_click(self):
        url = url_for(controller='text')
        res = self.app.get(url)
        res = res.click('Sonnet 18', index=0)
        assert 'Text - Info -' in res

