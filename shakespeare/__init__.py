'''
'''
__version__ = '0.7a'
__application_name__ = 'shakespeare'

def register_config(config_path):
    import os
    # TODO: remove? 2008-08-24 not mentioned in docs any more
    # envVarName = __application_name__.upper() + 'CONF'
    # config_path = os.environ.get(envVarName, '')
    config_path = os.path.abspath(config_path)
    import paste.deploy
    pasteconf = paste.deploy.appconfig('config:' + config_path)
    import shakespeare.config.environment
    shakespeare.config.environment.load_environment(pasteconf.global_conf,
        pasteconf.local_conf)


# TODO: rename to get_config()
def conf():
    from pylons import config
    conf = config
    return conf

def get_config():
    return conf()

