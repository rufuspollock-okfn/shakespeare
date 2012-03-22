from shakespeare.tests import *
from shakespeare import model

class TestOurResourceController(TestController):
    @classmethod
    def setup_class(self):
        TestData.make_fixture()

    @classmethod
    def teardown_class(self):
        TestData.remove_fixtures()

    def setup(self):
        self.text = model.Material.by_name(TestData.name)

    def test_index(self):
        res = self.app.get(url_for(controller='our_resource', action='index'))
        assert 'Resource' in res

    def test_view(self):
        reso = self.text.resources[0]
        offset = url_for(controller='our_resource', action='view',
                id=reso.id)
        res = self.app.get(offset)
        # can't do all of it as lines have formating added
        assert reso.locator[:5] in res, res

