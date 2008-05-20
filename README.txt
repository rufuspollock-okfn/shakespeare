Introduction
************

The Open Shakespeare package provides a full open set of shakespeare's works
(often in multiple versions) along with ancillary material, a variety of tools
and a python API.

Specifically in addition to the works themselves (often in multiple versions)
there is an introduction, a chronology, explanatory notes, a concordance and
search facilities.

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

Install ``shakespeare`` using easy_install::

    easy_install shakespeare

NB: If you don't have easy_install you can get from here:

<http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions>

Make a config file as follows::

    paster make-config shakespeare config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

1.2 (OR) Get the code straight from subversion
------------------------------------------------

1. Check out the subversion trunk::

    svn co https://knowledgeforge.net/shakespeare/svn/trunk

2. Do::

    sudo python setup.py develop


2. Cache Directory
==================

Create a cache directory where texts and other material can be stored

This directory needs to be semi-permanent so do *not* put under a location such
as /tmp. 



5. Initialize the system
========================

Run::

    $ shakespeare-admin db create
    $ shakespeare-admin db init

If you want to build the concordance do::

    $ shakespeare-admin concordance

NB: This may take some time to run so be patient. TIP: using sqlite building
the concordance really **does** seem to run forever so recommend using
postgresql or mysql if you are going to build the concordance. 


Getting Started
***************

As a user:
==========

Start up the web interface by running the webserver::

    $ paster serve {your-config.ini}

NB: {your-config.ini} should be replaced with the name of the config file you
created earlier.


As a developer:
===============

0. Copy development.ini.tmpl to development.ini and edit to your taste.

1. Check out the administrative commands: $ bin/shakespeare-admin help.

2. Run the tests using either py.test of nosetests::

    $ nosetests shakespeare

