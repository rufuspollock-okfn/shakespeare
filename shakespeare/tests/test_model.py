import sqlobject

import shakespeare.model as model

class TestMaterial(object):

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.url = 'http://www.openshakespeare.org/blah.txt'
        self.text = model.Material(name=self.name,
                title=self.title, url=self.url)

    @classmethod
    def teardown_class(self):
        model.Material.delete(self.text.id)
    
    def test1(self):
        txtid = self.text.id
        txt2 = model.Material.get(txtid)
        txt3 = model.Material.byName(self.name)
        assert self.text.id == txt2.id
        assert self.text.id == txt3.id
    
    def test_get_cache_path(self):
        out = self.text.get_cache_path('plain')
        # do not want anything too specific or we end up duplicating cache_test
        assert len(out) > 0

    def test_get_store_fileobj(self):
        text = model.Material.byName('phoenix_and_the_turtle_gut')
        out = text.get_store_fileobj()
        out = out.read()
        assert len(out) > 0
        assert out[:26] == 'THE PHOENIX AND THE TURTLE'


class TestConcordance(object):

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = model.Material(name=self.name, title=self.title)
        word = 'jones'
        line = 20
        char_index = 500
        self.cc1 = model.Concordance(text=self.text,
                                         word=word,
                                         line=line,
                                         char_index=char_index)

    @classmethod
    def teardown_class(self):
        model.Concordance.delete(self.cc1.id)
        model.Material.delete(self.text.id)

    def test1(self):
        out1 = model.Concordance.get(self.cc1.id)
        assert self.text == out1.text

class TestStatistic:

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = model.Material(name=self.name, title=self.title)
        self.word = 'jones'
        self.occurrences = 5
        self.cc1 = model.Statistic(
                text=self.text,
                word=self.word,
                occurrences=self.occurrences
                )

    @classmethod
    def teardown_class(self):
        model.Statistic.delete(self.cc1.id)
        model.Material.delete(self.text.id)

    def test1(self):
        out1 = model.Statistic.get(self.cc1.id)
        assert self.text == out1.text
        assert out1.occurrences == self.occurrences

    def test_select(self):
        tresults  = model.Statistic.select(
            sqlobject.AND(
                model.Statistic.q.textID == self.text.id,
                model.Statistic.q.word == self.word,
                ))
        num = tresults.count()
        assert num == 1

