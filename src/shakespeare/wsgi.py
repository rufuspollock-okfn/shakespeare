# wsgi applications interfaces

import shakespeare.wsgiplain

def app_factory(global_config, **local_conf):
    """Implement PasteDeploy's app_factory interface.
    """
    app = shakespeare.wsgiplain.ShakespeareWebInterface()
    return app

