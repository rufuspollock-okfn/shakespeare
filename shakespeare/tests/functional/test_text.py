from StringIO import StringIO

import pkg_resources

from shakespeare.tests import *
import shakespeare.model as model

class TestTextController(TestController):
    @classmethod
    def setup_class(cls):
        text = model.Material.byName('tempest_gut')
        if text is None:
            pkg = 'shksprdata'
            meta = pkg_resources.resource_stream(pkg, 'texts/metadata.txt')
            model.Material.load_from_metadata(meta)

    def test_index(self):
        url = url_for(controller='text')
        res = self.app.get(url)
        print res
        assert "Shakespeare's Works" in res
        assert 'The Tempest' in res

    def test_view_1(self):
        url = url_for(controller='text', action='view', name='tempest_gut',
            format='plain')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_index_2(self):
        url = url_for(controller='text')
        res = self.app.get(url)
        res = res.click('The Tempest', index=0)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_2(self):
        url = url_for(controller='text', action='view',
                name=['tempest_gut','tempest_gut_f'], format='plain')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_3(self):
        url = url_for(controller='text', action='view',
                name=['tempest_gut', 'tempest_gut_f'], format='raw')
        res = self.app.get(url)
        assert 'CALIBAN, a savage and deformed Slave' in res

    def test_view_with_unicode_source(self):
        url = url_for(controller='text', action='view',
                name='all_is_well_that_ends_well_gut_f', format='plain')
        res = self.app.get(url)
        assert "All's Well, that Ends Well" in res

