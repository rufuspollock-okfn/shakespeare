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

    def test_index(self):
        res = self.app.get(url_for(controller='anno', action='index'))
        assert 'Choose a text to annotate' in res
        res = res.click(self.text.work.title)
        assert 'Annotate' in res 
        assert self.text.content.split()[0] in res, res

    def test_annotate_no_text(self):
        res = self.app.get(url_for(controller='anno', action='annotate'),
            extra_environ={'REMOTE_USER': str(self.username)}
            )
        assert 'Annotate' in res
        assert 'No text to annotate' in res
    
    def test_annotate(self):
        res = self.app.get(
            url_for(controller='anno', action='annotate', id=self.text.name),
            extra_environ={'REMOTE_USER': str(self.username)}
            )
        assert "'uri': '%s'" % self.text.name
        userid = model.User.query.filter_by(openid=self.username).first().id
        assert "'user': '%s'" % userid

    # run this last
    def test_z_annotation(self):
        res = self.app.get(url_for(controller='anno_store', action='annotations'))
        # no annotations so []
        assert [] in res, res

