import unittest
import StringIO
import tempfile


import shakespeare.index
import shakespeare.concordance

def test_suite():
    suites = [
        unittest.makeSuite(ConcordancerTest),
        ]
    return unittest.TestSuite(suites)

class ConcordancerTest(unittest.TestCase):

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

    def setUp(self):
        self.builder = shakespeare.concordance.ConcordanceBuilder()
        # try deleting it first so as to be more robust to errors
        self.tearDown()
        self.text = shakespeare.dm.Material(name=self.name, title=self.title)
        self.builder.add_text(self.name, StringIO.StringIO(self.inText))
        self.concordance = shakespeare.concordance.Concordance([self.name])
        self.statistics = shakespeare.concordance.Statistics([self.name])

    def tearDown(self):
        # allow us to deal with left over stuff from previous errors
        try:
            self.builder.remove_text(self.name)
            tmp = shakespeare.dm.Material.byName(self.name)
            shakespeare.dm.Material.delete(tmp.id)
        except:
            pass

    def test__process_line(self):
        line = 'the - quick, brown. fox-jumped over$ the_lazy do8g.'
        exp = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the_lazy', 'do8g' ]
        out = self.builder.word_regex.findall(line)
        self.assertEqual(exp, out)

    def test_concordance(self):
        for key, value in self.expConcordance.items():
            listing = list(self.concordance.get(key))
            listing.reverse()
            out = [ (xx.text.name, xx.line, xx.char_index) for xx in listing ]
            self.assertEqual(out, value)

    def test_stats(self):
        for key, value in self.expStats.items():
            out = self.statistics.get(key)
            self.assertEqual(out, value)

    def test_keys(self):
        words = self.concordance.keys()
        self.assertEqual('a', words[0])
        self.assertEqual('your', words[-1])
        self.assertEqual(22, len(words))
