from annotator import auth
from shakespeare.lib.base import BaseController
from shakespeare.lib.base import abort, c, g, request, response


class TokenController(BaseController):

    def token(self):
        token = {
            'consumerKey': g.annotator_consumer_key,
            'ttl': 86400,
            'userId': c.author,
            'userIsAnonymous': c.user is None
        }

        response.headers['content-type'] = 'text/plain'
        return auth.encode_token(token, g.annotator_consumer_secret)
