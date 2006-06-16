Introduction
************

The Open Shakespeare package provides a complete set of shakespeare's works
(often in multiple versions) along with ancillary material and functionality
such as an introduction, chronology, explanatory notes and search facilities.

It provides all its material as open source and open knowledge so that anyone
is free to use, redistribute and reuse these materials freely. For exact
details of the license under which this package is made available please see
COPYING.txt.

Open Shakespeare has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/).


Contact the Project
*******************

Please mail shakespeare-info@okfn.org or join the okfn-discuss mailing list:

  http://lists.okfn.org/listinfo/okfn-discuss


Installation
************

1. Check out the subversion trunk
2. Add the path/to/src to your PYTHONPATH
3. Create a cache directory.
  1. create an environment variable CACHEDIR pointing to this directory e.g.
      $ export CACHEDIR=/path/to/cache
    * This directory needs to be semi-permanent so do *not* put under a
      location such as /tmp.
    * So that you do not always have to do the export every time you open a
      shell you might want to put it in your .bashrc file 
  2. Create a subdirectory of the cache directory named 'shakespeare'
4. Run $ bin/shakespeare-admin init
  * this may take some time to run so be patient

Getting Started
***************

As a user:
==========

Start up the web interface by running the webserver:
  $ cd path/to/trunk/src/shakespeare
  $ python cherrypy_handler.py

Then visit http://localhost:8080/ using your favourite web browser.

As a developer:
===============

1. Check out the administrative commands: $ bin/shakespeare-admin help.
2. Run the tests: python test.py


