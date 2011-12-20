Introduction
************

The Open Shakespeare package provides a full open set of shakespeare's works
(often in multiple versions) along with ancillary material, a variety of tools,
a python API and a web interface that provides access to many (but not all) of
these facilities from the comfort of your web browser (see
http://www.openshakespeare.org/).

All material is open source/open knowledge so that anyone can use, redistribute
and reuse these materials freely. For exact details of the license under which
this package is made available please see COPYING.txt.

Open Shakespeare has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/).

Contact the Project
*******************

Please mail open-shakespeare@okfn.org or join the open-literature mailing list:

  http://lists.okfn.org/listinfo/open-literature


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

You should also symlink who.ini into same directory as your config file.

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini
 
[TODO: this should be part of setup-app]

Run::

    $ shakespeare-admin db init


2. Web Interface
----------------

The graphical user interface is a web interface.

You can start a web server to provide a easy-to-use web interface to the
shakespeare material and facilities by doing::

    $ paster serve {your-config.ini}

NB: {your-config.ini} should be replaced with the name of the config file you
created earlier.


3. Commands and Command Line Interface
--------------------------------------

Main command line interface is via shakespeare-admin. Check it out by doing::

    shakespeare-admin help

In addition to shakespeare-admin commands there are also some paster commands.
To see what is available::

    paster -h


4. Extras
---------

1. To load the data packages, make sure you have downloaded and installed the
   relevant data package (e.g. shksprdata or miltondata) and then do::

    shakespeare-admin --config {your-ini-file} db init_shksprdata

2. Search index. To run the search index you will need xapian and the python
   xapian bindings installed. (On Debian/Ubuntu this is xapian and python-xapian).
   Then take a look at::

      shakespeare-admin search 

3. Word of the day. Enable this in your config file and then run
word_of_the_day command to pull the data.


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
