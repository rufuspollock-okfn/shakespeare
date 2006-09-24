from twill import commands as web

siteurl = 'http://localhost:8080/'

class TestSite:

    def test_index(self):
        web.go(siteurl)
        web.code(200)
        web.find('Index of Shakespeare plays')
        web.find('The Tempest')

    def test_view_1(self):
        url = siteurl + 'view?name=tempest_gut&format=plain'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_index_2(self):
        web.go(siteurl)
        web.follow('The Tempest')
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_view_2(self):
        url = siteurl + 'view?name=tempest_gut+tempest_gut_f&format=plain'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')

    def test_view_3(self):
        url = siteurl + 'view?name=tempest_gut+tempest_gut_f&format=raw'
        web.go(url)
        web.code(200)
        web.find('CALIBAN, a savage and deformed Slave')
 
