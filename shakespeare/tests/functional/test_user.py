from shakespeare.tests import *
import shakespeare.model as model

class TestUserController(TestController):
    @classmethod
    def setup_class(self):
        self.username = u'xyz.com'
        user = model.User(openid=self.username)
        model.Session.commit()
        self.userid = user.id
        model.Session.remove()

    @classmethod
    def teardown_class(self):
        user = model.User.query.get(self.userid)
        if user:
            model.Session.delete(user)
            model.Session.commit()
        model.Session.remove()

    def test_1_user_login(self):
        offset = url_for(controller='user', action='login')
        res = self.app.get(offset)
        assert 'User - Login' in res, res

    def test_2_user_not_logged_in(self):
        offset = url_for(controller='user', action='index')
        res = self.app.get(offset, '302')
        res = res.follow()
        assert 'User - Login' in res

    def test_2_user_logged_in(self):
        offset = url_for(controller='user', action='read', id=self.userid)
        res = self.app.get(offset, extra_environ={'REMOTE_USER':
            str(self.username)})
        assert 'User Account - %s' % self.username in res, res

    def test_logout(self):
        offset = url_for(controller='user', action='logout')
        res = self.app.get(offset)
        assert 'You have logged out successfully.' in res

