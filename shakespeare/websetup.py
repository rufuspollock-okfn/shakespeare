"""Setup the shakespeare application"""
import logging

from paste.deploy import appconfig
from pylons import config

from shakespeare.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup shakespeare here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    from shakespeare import model
    log.info('Creating tables')
    model.metadata.create_all(bind=model.meta.engine)
    log.info('Creating tables: SUCCESS')

