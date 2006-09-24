import shakespeare.dm

class TestMaterial:

    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.url = 'http://www.openshakespeare.org/blah.txt'
        self.text = shakespeare.dm.Material(name=self.name,
                title=self.title, url=self.url)

    def teardown_class(self):
        shakespeare.dm.Material.delete(self.text.id)
    
    def test1(self):
        txtid = self.text.id
        txt2 = shakespeare.dm.Material.get(txtid)
        txt3 = shakespeare.dm.Material.byName(self.name)
        assert self.text.id == txt2.id
        assert self.text.id == txt3.id
    
    def test_get_cache_path(self):
        out = self.text.get_cache_path('plain')
        # do not want anything too specific or we end up duplicating cache_test
        assert len(out) > 0

class TestConcordance:

    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = shakespeare.dm.Material(name=self.name, title=self.title)
        word = 'jones'
        line = 20
        char_index = 500
        self.cc1 = shakespeare.dm.Concordance(text=self.text,
                                         word=word,
                                         line=line,
                                         char_index=char_index)

    def teardown_class(self):
        shakespeare.dm.Concordance.delete(self.cc1.id)
        shakespeare.dm.Material.delete(self.text.id)

    def test1(self):
        out1 = shakespeare.dm.Concordance.get(self.cc1.id)
        assert self.text == out1.text

