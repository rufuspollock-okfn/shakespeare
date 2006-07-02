Introduction
************

The Open Shakespeare package provides a complete set of shakespeare's works
(often in multiple versions) along with ancillary material and functionality
such as an introduction, chronology, explanatory notes and search facilities.

All material is open source/open knowledge so that anyone can use, redistribute
and reuse these materials freely. For exact details of the license under which
this package is made available please see COPYING.txt.

Open Shakespeare has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/).


Contact the Project
*******************

Please mail shakespeare-info@okfn.org or join the okfn-discuss mailing list:

  http://lists.okfn.org/listinfo/okfn-discuss


Installation
************

1. Get the code
===============

1. Check out the subversion trunk
2. Add the path/to/src to your PYTHONPATH
3. Make sure you have all required dependencies:

  For the web interface:
    * cherrypy >= 2.2
    * kid templating language >= 0.9 (layout templates)

2. Cache Directory
==================

Create a cache directory where texts and other material can be stored

This directory needs to be semi-permanent so do *not* put under a location such
as /tmp. 

4. Create a configuration file
==============================

1. copy the template at etc/shakespeare.conf.new to a suitable new location
   (suggestion: etc/shakespeare.conf)

2. edit to reflect your setup (see comments in file)

3. make sure the config file can be found:
  1. EITHER: it must be located at etc/shakespeare.conf relative to the
       directory from which you run scripts
  
  2. OR: set the SHAKESPEARECONF environment variable to contain the path to
       the configuration file

4. Initialize the system
========================

Run: $ bin/shakespeare-admin init

This may take some time to run so be patient


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
2. Run the tests: python test.py


