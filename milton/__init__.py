__version__ = '0.1'
__application_name__ = 'milton'

def conf():
    import os
    defaultPath = os.path.abspath('./etc/%s.conf' % __application_name__)
    envVarName = __application_name__.upper() + 'CONF'
    confPath = os.environ.get(envVarName, defaultPath)
    if not os.path.exists(confPath):
        raise ValueError('No Configuration file exists at: %s' % confPath)
    import ConfigParser
    conf = ConfigParser.SafeConfigParser()
    conf.read(confPath)
    return conf

