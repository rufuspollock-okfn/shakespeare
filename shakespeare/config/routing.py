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

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE

    # Map the /admin url to FA's AdminController
    maps.admin_map(map, controller='admin', url='/admin')
    # now main shakespeare routes
    map.connect('', controller='site', action='index')
    map.connect('marginalia/*url', controller='site', action='marginalia')
    map.connect('material/:action/:id', controller='text')
    map.connect(':controller/:action/:id')
    map.connect(':action', controller='site')

    map.connect('*url', controller='template', action='view')

    return map
