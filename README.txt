Installation
************

1. Check out the subversion trunk
2. Add the path/to/src to your PYTHONPATH
3. Create a cache directory.
  * create an environment variable CACHEDIR pointing to this directory e.g.
      $ export CACHEDIR=/path/to/cache
    Note that this directory needs to be semi-permanent so do *not* put under a
    location such as /tmp.
  * Create a subdirectory of the cache directory named 'shakespeare'

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


