from shakespeare.tests import *
import shakespeare.model as model

class TestAnthologyController(TestController):
    @classmethod
    def setup_class(cls):
        TestData.make_fixture()
    
    @classmethod
    def teardown_class(cls):
        TestData.remove_fixtures()
        model.Session.remove()

    def test_index(self):
        response = self.app.get(url_for(controller='anthology', action='index'))
        assert 'Anthologies' in response, response
        form = response.forms[0]
        form['text'] = 'test_sonnet18'
        response = form.submit()
        assert 'Edit' in response, response
        assert 'Sonnet 18' in response, response

