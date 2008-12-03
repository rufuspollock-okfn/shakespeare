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

__all__ = ['url_for',
        'TestController', 'TestData', 'make_fixture', 'make_fixture2' ]

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

class TestData:
    name = 'test_sonnet18'
    name2 = 'test_sonnet18_2'

    @classmethod
    def make_fixture(self):
        import shakespeare.model as model
        sonnet18_work = model.Work.by_name(self.name)
        if not sonnet18_work:
            sonnet18_work = model.Work(name=self.name,
                    title='Sonnet 18',
                    creator='William Shakespeare'
                    )
        sonnet18 = model.Material.by_name(self.name)
        if not sonnet18:
            sonnet18 = model.Material(name=self.name,
                    title='Sonnet 18 (First Edition)',
                    work=sonnet18_work,
                    )
        assert len(sonnet18_work.materials)==1
        model.Session.flush()
        sonnet18.content = sonnet18_text
        return sonnet18

    @classmethod
    def make_fixture2(self):
        import shakespeare.model as model
        # work should exist by now
        sonnet18_work = model.Work.by_name(self.name)
        sonnet18 = model.Material.by_name(self.name2)
        if not sonnet18:
            sonnet18 = model.Material(name=self.name2,
                    title='Sonnet 18 Duplicate',
                    work=sonnet18_work
                    )
            model.Session.flush()
        sonnet18.content = sonnet18_text
        return sonnet18

    @classmethod
    def remove_fixtures(self):
        import shakespeare.model as model
        # work should exist by now
        for n in [ self.name, self.name2 ]:
            m = model.Material.by_name(n)
            if m:
                model.Session.delete(m)
        w = model.Work.by_name(self.name)
        if w:
            model.Session.delete(w)
        model.Session.flush()


make_fixture = TestData.make_fixture
make_fixture2 = TestData.make_fixture2


class TestController(object):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(wsgiapp)
