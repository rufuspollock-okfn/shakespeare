from shakespeare.tests import *
import shakespeare.model as model

class TestWordController(TestController):
    @classmethod
    def setup_class(self):
        ns = u'word'
        self.word = u'incardine'
        self.notes = u'''### About

xxxxxxxxxxxxxxx'''
        model.KeyValue(ns=ns, object_id=self.word, key=u'notes',
                value=self.notes)
        model.Session.commit()

    @classmethod
    def teardown_class(self):
        for kv in model.Session.query(model.KeyValue):
            model.Session.delete(kv)
        model.Session.commit()
        model.Session.remove()

    def test_index(self):
        res = self.app.get(url(controller='word', action='index'))
        assert 'Words - Index' in res

    def test_read(self):
        res = self.app.get(url(controller='word', action='read', id=self.word))
        assert self.word.capitalize() in res, res
        # notes
        assert '<h3>About' in res, res
        assert 'Statistics for %s' % self.word in res, res
        assert 'Search works for %s' % self.word in res, res

