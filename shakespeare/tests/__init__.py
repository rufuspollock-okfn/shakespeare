"""Pylons application test package

When the test runner finds and executes tests within this directory,
this file will be loaded to setup the test environment.

It registers the root directory of the project in sys.path and
pkg_resources, in case the project hasn't been installed with
setuptools. It also initializes the application via websetup (paster
setup-app) with the project's test.ini configuration file.
"""
import os
import sys

import pkg_resources
import paste.fixture
import paste.script.appinstall
from paste.deploy import loadapp
from routes import url_for

__all__ = ['url_for', 'TestController', 'make_fixture' ]

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)
pkg_resources.working_set.add_entry(conf_dir)
pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

test_file = os.path.join(conf_dir, 'test.ini')
cmd = paste.script.appinstall.SetupCommand('setup-app')
cmd.run([test_file])

sonnet18_text = \
'''Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:

Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd,
And every fair from fair sometime declines,
By chance, or nature's changing course untrimm'd: 

But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st,
Nor shall death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st,

  So long as men can breathe, or eyes can see,
  So long lives this, and this gives life to thee.
'''

# must use make_fixture rather than just create object as we need to be in
# current db session
def make_fixture():
    import shakespeare.model as model
    sonnet18_name = 'test_sonnet18'
    sonnet18 = model.Material.byName(sonnet18_name)
    if not sonnet18:
        sonnet18 = model.Material(name=sonnet18_name,
                title='Sonnet 18',
                )
        model.Session.flush()
    sonnet18.content = sonnet18_text
    return sonnet18


class TestController(object):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(wsgiapp)
