import shakespeare.model as model

class TestWorkAndMaterial(object):

    @classmethod
    def setup_class(self):
        self.name = u'test-123'
        self.title = u'Hamlet'
        work = model.Work(
            name=self.name,
            title=self.title)
        text = model.Material(
            title=self.title,
            work=work,
            )
        resource = model.Resource(
            material=text,
            locator_type=u'package',
            locator=u'shksprdata::/gutenberg/phoenix_and_the_turtle_gut.txt',
            format=u'txt',
            )

        model.Session.flush()
        self.workid = work.id
        self.textid = text.id
        self.resourceid = resource.id
        model.Session.clear()

    @classmethod
    def teardown_class(self):
        model.repo.rebuild_db()
    
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
        assert txt2.resources
    
    def test_get_text(self):
        text = model.Material.query.get(self.textid)
        out = text.get_text()
        out = out.read()
        assert len(out) > 0
        assert out[:26] == 'THE PHOENIX AND THE TURTLE'

    def test_resource(self):
        res = model.Resource.query.get(self.resourceid)
        assert res.format == u'txt'


class TestResource:
    def test_get_stream_inline(self):
        sometext = u'aaaaaaaaaaaaa'
        res = model.Resource(locator=sometext, locator_type=u'inline')
        out = res.get_stream()
        assert out.read() == sometext


class TestStatistic:

    @classmethod
    def setup_class(self):
        self.name = u'test-123'
        self.title = u'Hamlet'
        self.text = model.Material(name=self.name, title=self.title)
        self.word = u'jones'
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

