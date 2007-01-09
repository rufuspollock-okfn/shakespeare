from StringIO import StringIO

import twill
from twill import commands as web

import shakespeare.wsgi


class TestSite:

    port = 8080
    siteurl = 'http://localhost:8080/'

    def setup_method(self, name=''):
        wsgi_app = shakespeare.wsgi.app_factory(global_config=None)
        twill.add_wsgi_intercept('localhost', self.port, lambda : wsgi_app)
        self.outp = StringIO()
        twill.set_output(self.outp)

    def teardown_method(self, name=''):
        # remove intercept.
        twill.remove_wsgi_intercept('localhost', self.port)

    def test_index(self):
        web.go(self.siteurl)
        print web.show()
        web.code(200)
        web.find('Index of Shakespeare plays')
        web.find('The Tempest')

    def test_view_1(self):
        url = self.siteurl + 'view?name=tempest_gut&format=plain'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_index_2(self):
        web.go(self.siteurl)
        web.follow('The Tempest')
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_view_2(self):
        url = self.siteurl + 'view?name=tempest_gut+tempest_gut_f&format=plain'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_view_3(self):
        url = self.siteurl + 'view?name=tempest_gut+tempest_gut_f&format=raw'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_view_with_unicode_source(self):
        url = self.siteurl + 'view?name=all_is_well_that_ends_well_gut_f&format=plain'
        web.go(url)
        web.code(200)
        web.find("All's Well, that Ends Well")

    def test_guide(self):
        url = self.siteurl + 'guide/'
        web.go(url)
        web.code(200)
        web.find('guide to the features of the Open Shakespeare web')

    def test_concordance(self):
        url = self.siteurl + 'concordance/'
        web.go(url)
        web.code(200)
 
