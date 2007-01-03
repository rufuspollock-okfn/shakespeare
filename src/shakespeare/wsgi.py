# wsgi applications interfaces

def setup_cherrypy():
    # this is for cherrypy 3.0
    # for more information including how to set up fastcgi see
    # http://www.cherrypy.org/wiki/FastCGIWSGI
    import cherrypy
    import shakespeare.cherrypy_handler 
    app = cherrypy.tree.mount(shakespeare.cherrypy_handler.ShakespeareWebInterface())
    # does not seem to be needed for wsgi stuff
    # cherrypy.server.quickstart()
    cherrypy.engine.start(blocking=False)
    return app

def app_factory(global_config, **local_conf):
    """Implement PasteDeploy's app_factory interface.
    """
    app = setup_cherrypy() 
    return app

