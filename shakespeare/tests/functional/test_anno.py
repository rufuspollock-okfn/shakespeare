from shakespeare.tests import *
import shakespeare.model as model

class TestAnnoController(TestController):
    @classmethod
    def setup_class(self):
        self.text = TestData.make_fixture()
        self.username = u'xyz.com'

    @classmethod
    def teardown_class(self):
        model.repo.rebuild_db()

    def test_annotate_no_text(self):
        res = self.app.get(
            url_for(controller='work', action='annotate'),
            extra_environ={'REMOTE_USER': str(self.username)},
            status=[404]
        )

