# wsgi applications interfaces

import milton.wsgiplain

def app_factory(global_config, **local_conf):
    """Implement PasteDeploy's app_factory interface.
    """
    app = milton.wsgiplain.MiltonWebInterface()
    return app

