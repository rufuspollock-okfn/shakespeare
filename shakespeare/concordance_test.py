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
A fake imperial line.
"""
    name = 'test-concordance'
    title = 'Hamlet'
    
    # ['work_id', 'line-no', 'character-index'] }
    # incomplete
    expConcordance = {
        'fake' : [ (name, 0, 2), (name, 0, 7), (name, 5, 136) ],
        'suffolk' : [ (name, 1, 17), ],
        'high' : [ (name, 2, 37), ],
        'word_that_is_not_there' : [],
        }

    # incomplete
    expStats = {
        'fake' : 3,
        'imperial' : 2,
        'suffolk' : 1,
        'high' : 1,
        'word_that_is_not_there' : 0,
        }

    @classmethod
    def setup_class(cls):
        cls.builder = shakespeare.concordance.ConcordanceBuilder()
        # try deleting it first so as to be more robust to errors
        # does not seem to work with the class methods
        # cls.teardown_class(cls)
        cls.text = shakespeare.model.Material(name=cls.name, title=cls.title)
        cls.builder.add_text(cls.name, StringIO.StringIO(cls.inText))
        cls.concordance = shakespeare.concordance.Concordance([cls.name])
        cls.statistics = shakespeare.concordance.Statistics([cls.name])

    @classmethod
    def teardown_class(cls):
        # allow us to deal with left over stuff from previous errors
        try:
            cls.builder.remove_text(cls.name)
            tmp = shakespeare.model.Material.byName(cls.name)
            shakespeare.model.Material.delete(tmp.id)
        except:
            pass

    def test__process_line(self):
        line = 'the - quick, brown. fox-jumped over$ the_lazy do8g.'
        exp = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the_lazy', 'do8g' ]
        out = self.builder.word_regex.findall(line)
        assert exp == out

    def test_is_roman_numeral(self):
        testvals = [ 'ii', 'v', 'vi', 'xi', 'xx', 'xxi', 'xlvi', 'c', 'cvi' ]
        for val in testvals:
            assert self.builder.is_roman_numeral(val)

    def test_ignore_word(self):
        testvals = [ 'd', 't' ]
        for val in testvals:
            assert self.builder.ignore_word(val)

    def test_concordance(self):
        for key, value in self.expConcordance.items():
            listing = list(self.concordance.get(key))
            assert len(listing) == len(value)
            for xx in listing:
                assert (xx.text.name, xx.line, xx.char_index) in value

    def test_stats(self):
        for key, value in self.expStats.items():
            out = self.statistics.get(key)
            print key
            assert out == value

    def test_keys(self):
        words = self.concordance.keys()
        assert 'a' == words[0]
        assert 'your' == words[-1]
        assert 22 == len(words)
