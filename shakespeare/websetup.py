"""Setup the shakespeare application"""
import logging

from shakespeare.config.environment import load_environment
import shakespeare.model import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup shakespeare here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info('Creating tables')
    model.repo.create_db()
    log.info('Creating tables: SUCCESS')

