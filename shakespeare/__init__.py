__version__ = '0.5dev'
__application_name__ = 'shakespeare'

def conf():
    import os
    defaultPath = os.path.abspath('./development.ini')
    envVarName = __application_name__.upper() + 'CONF'
    confPath = os.environ.get(envVarName, defaultPath)
    if not os.path.exists(confPath):
        raise ValueError('No Configuration file exists at: %s' % confPath)

    # register the config
    import paste.deploy
    import shakespeare.config.environment
    pasteconf = paste.deploy.appconfig('config:' + confPath)

    shakespeare.config.environment.load_environment(pasteconf.global_conf,
        pasteconf.local_conf)
    from pylons import config
    conf = config

    # import ConfigParser
    # conf = ConfigParser.SafeConfigParser()
    # conf.read(confPath)

    return conf
     
