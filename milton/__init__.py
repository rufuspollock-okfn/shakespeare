'''
Introduction
************

The Open Milton package provides a full open set of shakespeare's works
(often in multiple versions) along with ancillary material, a variety of tools
and a python API.

Specifically in addition to the works themselves (often in multiple versions)
there is an introduction, a chronology, explanatory notes, a concordance and
search facilities.

All material is open source/open knowledge so that anyone can use, redistribute
and reuse these materials freely. For exact details of the license under which
this package is made available please see COPYING.txt.

Open Milton has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/). It is a sub-project of Open Shakespeare.

Contact the Project
*******************

Please mail info@okfn.org or join the okfn-discuss mailing list:

  http://lists.okfn.org/listinfo/okfn-discuss


Installation and Setup
**********************

1. Install the code
===================

1.1: (EITHER) Install using setup.py (preferred)
------------------------------------------------

Install ``milton`` using easy_install::

    easy_install shakespeare

NB: If you don't have easy_install you can get from here:

<http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions>


1.2 (OR) Get the code straight from subversion
------------------------------------------------

1. Check out the subversion trunk::

    svn co https://knowledgeforge.net/shakespeare/svn/trunk

2. Do::

    sudo python setup.py develop


Getting Started
***************

As a user:
==========

1. Basic setup
--------------

To access most of the main features of Open Milton you need a database.
For this an other bits and bobs of configuration you will need a configuration
file.

You can make a config file as follows::

    paster make-config milton {your-config.ini}

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini
 
[TODO: this should be part of setup-app]

Run::

    $ milton-admin db create
    $ milton-admin db init

2. Extras
---------

1. Search index. [TODO]

2. You can start a web server to provide a easy-to-use web interface to the
shakespeare material and facilities by doing::

    $ paster serve {your-config.ini}

NB: {your-config.ini} should be replaced with the name of the config file you
created earlier.


As a developer:
===============

0. Setup
--------

Follow the basic steps above put with an ini file named: development.ini

NB: you'll probably want to change log levels to debug.

1. Check out the administrative commands
----------------------------------------

    $ bin/milton-admin help.

2. Run the tests using either py.test of nosetests::
----------------------------------------------------

    $ nosetests milton
'''
__version__ = '0.2dev'
__application_name__ = 'milton'

def conf():
    import os
    defaultPath = os.path.abspath('./development.ini')
    envVarName = __application_name__.upper() + 'CONF'
    confPath = os.environ.get(envVarName, defaultPath)
    if not os.path.exists(confPath):
        raise ValueError('No Configuration file exists at: %s' % confPath)

    # register the config
    import paste.deploy
    import milton.config.environment
    pasteconf = paste.deploy.appconfig('config:' + confPath)

    milton.config.environment.load_environment(pasteconf.global_conf,
        pasteconf.local_conf)
    from pylons import config
    conf = config

    # import ConfigParser
    # conf = ConfigParser.SafeConfigParser()
    # conf.read(confPath)

    return conf

