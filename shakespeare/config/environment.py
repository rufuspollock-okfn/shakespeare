"""Pylons environment configuration"""
import os

from genshi.template import TemplateLoader
from pylons import config
from sqlalchemy import engine_from_config

import shakespeare.lib.app_globals as app_globals
import shakespeare.lib.helpers
from shakespeare.config.routing import make_map
from shakespeare.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='shakespeare', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = shakespeare.lib.helpers

    # redo template setup to use genshi.search_path (so remove std template setup)
    # This requires path notation in calls to render rather than dotted notation
    # e.g. render('index.html') not render('index') etc
    # See:
    # http://genshi.edgewall.org/wiki/Documentation/0.5.x/plugin.html#template-paths
    # http://wiki.pylonshq.com/display/pylonscookbook/Template+plugins+(for+developers)
    # esp section: History, dotted notation vs URI notation, and the future
#    genshi = config['buffet.template_engines'].pop()
#    # set None for template_root as not using dotted (python package) notation
#    config.add_template_engine('genshi', None)
#
#    tmpl_options = config['buffet.template_options']
    template_paths = [paths['templates'][0]]
    extra_template_paths = app_conf.get('extra_template_paths', '')
    if extra_template_paths:
        # must be first for them to override defaults
        template_paths = extra_template_paths.split(',') + template_paths
    # tmpl_options['genshi.search_path'] = ':'.join(template_paths) 

    # Create the Genshi TemplateLoader
    # config['pylons.app_globals'].genshi_loader = TemplateLoader(
    #    paths['templates'], auto_reload=True)
    config['pylons.app_globals'].genshi_loader = TemplateLoader(
        template_paths, auto_reload=True)

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
