from shakespeare.tests import *
import jwt

class TestTokenController(TestController):

    def test_token(self):
        response = self.app.get(url_for(controller='token', action='token'), extra_environ={'REMOTE_ADDR': '8.8.8.8'})
        token = jwt.decode(response.body, verify=False)

        assert 'consumerKey' in token
        assert token['userId'] == '8.8.8.8'
        assert token['userIsAnonymous'] == True
        assert token['ttl'] == 86400

    def test_token_no_ip(self):
        response = self.app.get(url_for(controller='token', action='token'))
        token = jwt.decode(response.body, verify=False)

        assert 'consumerKey' in token
        assert token['userId'] == 'Unknown IP Address'
        assert token['userIsAnonymous'] == True
        assert token['ttl'] == 86400

    def test_token_logged_in(self):
        response = self.app.get(url_for(controller='token', action='token'), extra_environ={'REMOTE_USER': 'alice'})
        token = jwt.decode(response.body, verify=False)

        assert 'consumerKey' in token
        assert token['userId'] == 'alice'
        assert token['userIsAnonymous'] == False
        assert token['ttl'] == 86400
