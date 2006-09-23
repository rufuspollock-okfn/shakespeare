import shakespeare.moby

class TestIndex(object):
    index = shakespeare.moby.index

    def test_index(self):
        title = 'Twelfth Night'
        url = 'http://www.ibiblio.org/xml/examples/shakespeare/t_night.xml'
        assert (title, url) in self.index
        assert len(self.index) == 37

class TestHelper(object):
    helper = shakespeare.moby.Helper()
    url1 = 'http://www.ibiblio.org/xml/examples/shakespeare/t_night.xml'

    def test_download(self):
        self.helper.download(self.url1)
        self.helper.download()

    def test_add_to_db(self):
        self.helper.add_to_db()
        text1 = shakespeare.dm.Material.byName('hamlet_moby')
        assert text1.creator == 'Shakespeare, William'
        assert text1.title == 'Hamlet'

