import shakespeare.model as model

class TestWorkAndMaterial(object):

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        work = model.Work(
            name=self.name,
            title=self.title)
        text = model.Material(
            title=self.title,
            work=work,
            src_pkg='shksprdata',
            src_locator='/gutenberg/phoenix_and_the_turtle_gut.txt'
            )

        model.Session.flush()
        self.workid = work.id
        self.textid = text.id
        model.Session.clear()

    @classmethod
    def teardown_class(self):
        text = model.Material.query.get(self.textid)
        work = model.Material.query.get(self.workid)
        model.Session.delete(text)
        if work:
            model.Session.delete(work)
        model.Session.flush()
    
    def test_work(self):
        work = model.Work.query.get(self.workid)
        work2 = model.Work.by_name(self.name)
        assert work.title == self.title
        assert work2.title == self.title
        assert len(work.materials) == 1

    def test_material(self):
        txt2 = model.Material.query.get(self.textid)
        assert txt2.title == self.title
        assert txt2.work.id == self.workid
    
    def test_get_text(self):
        text = model.Material.query.get(self.textid)
        out = text.get_text()
        out = out.read()
        assert len(out) > 0
        assert out[:26] == 'THE PHOENIX AND THE TURTLE'


class TestStatistic:

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = model.Material(name=self.name, title=self.title)
        self.word = 'jones'
        self.freq = 5
        self.cc1 = model.Statistic(
                text=self.text,
                word=self.word,
                freq=self.freq
                )
        model.Session.flush()
        self.statid = self.cc1.id
        model.Session.clear()

    @classmethod
    def teardown_class(self):
        stat = model.Statistic.query.get(self.statid)
        model.Session.delete(stat)
        model.Session.delete(stat.text)
        model.Session.flush()
        model.Session.remove()

    def test1(self):
        out1 = model.Statistic.query.get(self.statid)
        assert out1.text.name == self.name
        assert out1.freq == self.freq

    def test_select(self):
        tresults = model.Statistic.query.filter_by(text=self.text
                ).filter_by(word=self.word)
        num = tresults.count()
        assert num == 1

