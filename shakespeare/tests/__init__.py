"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import config, url
from routes.util import URLGenerator
from webtest import TestApp

import pylons.test

__all__ = ['environ', 'url', 'url_for', 'TestController', 'TestData',
        'make_fixture', 'make_fixture2' ]

environ = {}
# rgrp: for backwards compatibility (pre pylons 0.9.7) alias url_for to url
url_for = url

# rgrp: rather than set up with websetup rebuild the db
# Invoke websetup with the current config file
# SetupCommand('setup-app').run([config['__file__']])
# import shakespeare
# shakespeare.register_config(test_file)
import shakespeare.model as model
model.repo.rebuild_db()

sonnet18_text = \
u'''Shall I compare thee to a summer's day?
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
    name = u'test_sonnet18'
    name2 = u'test_sonnet18_2'

    @classmethod
    def make_fixture(self):
        import shakespeare.model as model
        sonnet18_work = model.Work.by_name(self.name)
        if not sonnet18_work:
            sonnet18_work = model.Work(name=self.name,
                    title=u'Sonnet 18',
                    creator=u'William Shakespeare'
                    )
        sonnet18 = model.Material.by_name(self.name)
        if not sonnet18:
            sonnet18 = model.Material(name=self.name,
                    title=u'Sonnet 18 (First Edition)',
                    work=sonnet18_work,
                    )
        if not sonnet18.resources:
            res = model.Resource(locator_type=u'inline',
                locator=sonnet18_text,
                format=u'txt')
            sonnet18.resources.append(res)
        assert len(sonnet18_work.materials)==1
        model.Session.commit()
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
                    title=u'Sonnet 18 Duplicate',
                    work=sonnet18_work
                    )
            model.Session.commit()
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
        model.Session.commit()


make_fixture = TestData.make_fixture
make_fixture2 = TestData.make_fixture2


class TestController(object):

    def __init__(self, *args, **kwargs):
        if pylons.test.pylonsapp:
            wsgiapp = pylons.test.pylonsapp
        else:
            wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))

