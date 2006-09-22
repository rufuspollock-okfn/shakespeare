import unittest
import StringIO
import tempfile


import shakespeare.index
import shakespeare.concordance

class TestConcordancer:

    inText = \
"""A fake fake line
SUFFOLK.
As by your high imperial Majesty
I had in charge at my depart for France,
As procurator to your excellence,
"""
    name = 'test-concordance'
    title = 'Hamlet'
    
    # ['work_id', 'line-no', 'character-index'] }
    expConcordance = {
        'fake' : [ (name, 0, 2), (name, 0, 7) ],
        'suffolk' : [ (name, 1, 17), ],
        'high' : [ (name, 2, 37), ],
        'word_that_is_not_there' : [],
        }

    expStats = {
        'fake' : 2,
        'suffolk' : 1,
        'high' : 1,
        'word_that_is_not_there' : 0,
        }

    def setup_class(cls):
        cls.builder = shakespeare.concordance.ConcordanceBuilder()
        # try deleting it first so as to be more robust to errors
        # does not seem to work with the class methods
        # cls.teardown_class(cls)
        cls.text = shakespeare.dm.Material(name=cls.name, title=cls.title)
        cls.builder.add_text(cls.name, StringIO.StringIO(cls.inText))
        cls.concordance = shakespeare.concordance.Concordance([cls.name])
        cls.statistics = shakespeare.concordance.Statistics([cls.name])

    def teardown_class(cls):
        # allow us to deal with left over stuff from previous errors
        try:
            cls.builder.remove_text(cls.name)
            tmp = shakespeare.dm.Material.byName(cls.name)
            shakespeare.dm.Material.delete(tmp.id)
        except:
            pass

    def test__process_line(self):
        line = 'the - quick, brown. fox-jumped over$ the_lazy do8g.'
        exp = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the_lazy', 'do8g' ]
        out = self.builder.word_regex.findall(line)
        assert exp == out

    def test_concordance(self):
        for key, value in self.expConcordance.items():
            listing = list(self.concordance.get(key))
            listing.reverse()
            out = [ (xx.text.name, xx.line, xx.char_index) for xx in listing ]
            assert out == value

    def test_stats(self):
        for key, value in self.expStats.items():
            out = self.statistics.get(key)
            assert out == value

    def test_keys(self):
        words = self.concordance.keys()
        assert 'a' == words[0]
        assert 'your' == words[-1]
        assert 22 == len(words)
