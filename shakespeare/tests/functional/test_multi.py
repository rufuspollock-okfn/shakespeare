from StringIO import StringIO

from shakespeare.tests import *

class TestMultiController(TestController):
    @classmethod
    def setup_class(self):
        self.text = TestData.make_fixture()

    @classmethod
    def teardown_class(self):
        TestData.remove_fixtures()

    def test_index(self):
        url = url_for(controller='multi', action='index')
        res = self.app.get(url)
        print res
        assert 'Multiview' in res
    
    def test_choose_texts(self):
        url = url_for(controller='multi', action='index')
        res = self.app.get(url)
        form = res.forms[1]
        print self.text.name
        form['text_1'] = self.text.name
        form['text_2'] = self.text.name
        res = form.submit() 
        print res.request.url
        assert 'Multiview - View' in res
        # TODO: 2009-07-16 this should be uncommented
        # however form setting does not seem to work (don't know why!)
        assert not 'Error' in res, res
   
    def test_view(self):
        url = url_for(controller='multi', action='index',
                text_1=self.text.name, text_2=self.text.name)
        res = self.app.get(url)
        assert self.text.name in res

