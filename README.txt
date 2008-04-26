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


3. Create a configuration file
==============================

1. copy the template at etc/shakespeare.conf.new to a suitable new location
   (suggestion: etc/shakespeare.conf)

2. edit to reflect your setup (see comments in file)

3. make sure the config file can be found:
  1. EITHER: it must be located at etc/shakespeare.conf relative to the
       directory from which you run scripts
  
  2. OR: set the SHAKESPEARECONF environment variable to contain the path to
       the configuration file


5. Initialize the system
========================

Run: $ bin/shakespeare-admin init

This may take some time to run so be patient

TIP: using sqlite building the concordance really **does** seem to run forever
so recommend using postgresql or mysql if you are going to build the
concordance. 


Getting Started
***************

As a user:
==========

Start up the web interface by running the webserver:

  $ bin/shakespeare-admin runserver

Then visit http://localhost:8080/ using your favourite web browser.

As a developer:
===============

1. Check out the administrative commands: $ bin/shakespeare-admin help.

2. Run the tests: $ py.test
   
Note that:
   
  * The tests use [py.test] so you will need to have installed this

  * To run the website tests (site_test etc) you will need to install [twill]
    and have the webserver running

[py.test]: http://codespeak.net/py/current/doc/getting-started.html
[twill]: http://twill.idyll.org/

