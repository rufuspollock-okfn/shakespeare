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

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    # Map the /admin url to FA's AdminController
    maps.admin_map(map, controller='admin', url='/admin')
    # now main shakespeare routes
    map.connect('pdf', 'pdf/*url')
    map.connect('home', '/', controller='site', action='index')
    map.connect('about', '/about/', controller='site', action='about')
    map.connect('news', '/news/', controller='site', action='news')
    map.connect('get-involved', '/get-involved/', controller='site', action='about')
    map.connect('wotw', '/wotw/{url:.*}', controller='site', action='wotw')
    map.connect('guide', '/guide/', controller='site', action='guide')
    map.connect('/resource/{action}/{id}{url:.*}', controller='our_resource')
    map.connect('/resource/{action}/{id}', controller='our_resource')
    map.connect('/material/{action}/{id}', controller='text')
    # Annotation store requires requests at /anno_store/annotation/
    map.connect('/anno_store/{action}/{url:.*}', controller='anno_store')
    map.connect('/{controller}/', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    map.connect('/*url', controller='template', action='view')

    return map
