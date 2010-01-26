'''
Introduction
************

The Open Shakespeare package provides a full open set of shakespeare's works
(often in multiple versions) along with ancillary material, a variety of tools,
a python API and a web interface that provides access to many (but not all) of
these facilities from the comfort of your web browser (see
http://www.openshakespeare.org/ for a demo).

All material is open source/open knowledge so that anyone can use, redistribute
and reuse these materials freely. For exact details of the license under which
this package is made available please see COPYING.txt.

Open Shakespeare has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/).

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

Install ``shakespeare`` using easy_install (or pip)::

    easy_install shakespeare
    # or
    pip install shakespeare

NB: If you don't have easy_install you can get from here:

<http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions>


1.2 (OR) Get the code straight from the repository
--------------------------------------------------

1. Check out the mercurial repo::

    hg clone https://knowledgeforge.net/shakespeare/hg

2. Do::

    python setup.py develop


Getting Started
***************

As a user:
==========

1. Basic setup
--------------

To access most of the main features of Open Shakespeare you need a database.
For this an other bits and bobs of configuration you will need a configuration
file.

You can make a config file as follows::

    paster make-config shakespeare {your-config.ini}

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini
 
[TODO: this should be part of setup-app]

Run::

    $ shakespeare-admin db init

2. Extras
---------

1. Search index. [TODO]

2. To load the author packages, change into the miltondata or shksprdata directories
   and run the command load-milton (or load-shakespeare) -c <path to your
   development.ini> This will load the metadata text into the database. 

3. You can start a web server to provide a easy-to-use web interface to the
   shakespeare material and facilities by doing::

        $ paster serve {your-config.ini}

   NB: {your-config.ini} should be replaced with the name of the config file you
created earlier.


As a developer:
===============

0. Setup
--------

Follow the basic steps above but with an ini file named: development.ini

NB: you'll probably want to change log levels to debug.

1. Check out the administrative commands
----------------------------------------

    $ bin/shakespeare-admin help.

2. Run the tests using either py.test of nosetests::
----------------------------------------------------

    $ nosetests shakespeare
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

