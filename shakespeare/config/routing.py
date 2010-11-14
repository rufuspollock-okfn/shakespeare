"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper
from formalchemy.ext.pylons import maps # routes generator

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = True

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    # Map the /admin url to FA's AdminController
    maps.admin_map(map, controller='admin', url='/admin')
    # now main shakespeare routes
    map.connect('pdf', 'pdf/*url')
    if bool(config.get('deliverance.enabled', '')):
        map.connect('home', '/', controller='template', action='view', url='/')
        map.connect('about', '/about', controller='template', action='view',
                url='/about')
    else:
        map.connect('home', '/', controller='site', action='index')
        map.connect('about', '/about', controller='index', action='about')
    map.connect('/resource/{action}/{id}', controller='our_resource')
    map.connect('/material/{action}/{id}', controller='text')
    # Annotation store requires requests at /anno_store/annotation/
    map.connect('/anno_store{url:.*}', controller='anno_store', action='view')

    map.redirect("/word/read/{id}", "/word/{id}")
    map.connect('/word', controller='word', action='index')
    map.connect('/word/{id}', controller='word', action='read')

    map.connect('/work', controller='work', action='index')
    map.connect('/work/info/{id}', controller='work', action='info')
    map.connect('/work/annotate/{id}', controller='work', action='annotate')
    map.connect('/work/{id}', controller='work', action='view')

    map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    map.redirect('/*(url)/', '/{url}',
                 _redirect_code='301 Moved Permanently')
    # make sure we do not match repoze.who.openid urls
    def exclude(environ, result):
        if environ.get('PATH_INFO') in ['/login_openid', '/logout_openid']:
            return False
        else:
            return True
    map.connect('/*url', controller='template', action='view',
            conditions=dict(function=exclude))
    return map

