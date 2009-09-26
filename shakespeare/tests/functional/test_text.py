from StringIO import StringIO

from shakespeare.tests import *
import shakespeare.model as model

class TestTextController(TestController):
    @classmethod
    def setup_class(cls):
        text = model.Material.byName(u'tempest_gut')
        if text is None:
            print 'Adding items'
            import shksprdata.cli
            shksprdata.cli.LoadTexts.load_texts()
            model.Session.flush()
            model.Session.remove()
        assert len(model.Material.query.all()) > 20
    
    @classmethod
    def teardown_class(cls):
        all = model.Material.query.all()
        for m in all:
            model.Session.delete(m)
        model.Session.flush()
        model.Session.remove()

    def test_index(self):
        url = url_for(controller='text', action='index', id=None)
        res = self.app.get(url)
        print res
        assert 'Texts - Index' in res
        assert 'The Tempest' in res

    def test_info(self):
        url = url_for(controller='text', action='info', id='tempest_gut')
        res = self.app.get(url)
        assert 'tempest_gut' in res, res

    def test_view_1(self):
        url = url_for(controller='text', action='view', id='tempest_gut',
            format='plain')
        res = self.app.get(url)
        res = res.follow()
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_index_click(self):
        url = url_for(controller='text')
        res = self.app.get(url)
        res = res.click('The Tempest', index=0)
        assert 'Text - Info -' in res

    def test_index_click_view(self):
        url = url_for(controller='text')
        res = self.app.get(url)
        res = res.click('view', index=0)
        res = res.follow()
        assert "All's Well, that Ends Well" in res, res[:1000]

    def test_view_with_unicode_source(self):
        url = url_for(controller='text', action='view',
                id='all_is_well_that_ends_well_gut_f')
        res = self.app.get(url)
        res = res.follow()
        assert "All's Well, that Ends Well" in res

