import unittest
import StringIO
import tempfile


import shakespeare.index
import shakespeare.concordancer

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
        self.text = shakespeare.dm.Material(name=self.name, title=self.title)
        self.builder = shakespeare.concordancer.ConcordanceBuilder()
        self.builder.add_text(self.name, StringIO.StringIO(self.inText))
        self.concordance = shakespeare.concordancer.Concordance()
        self.statistics = shakespeare.concordancer.Statistics()

    def tearDown(self):
        shakespeare.dm.Material.delete(self.text.id)

    def test__process_line(self):
        line = 'the - quick, brown. fox-jumped over$ the_lazy do8g.'
        exp = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the_lazy', 'do8g' ]
        out = self.builder.word_regex.findall(line)
        self.assertEqual(exp, out)

    def test_concordance(self):
        for key, value in self.expConcordance.items():
            listing = list(self.concordance.get(key))
            out = [ (xx.text.name, xx.line, xx.char_index) for xx in listing ]
            self.assertEqual(out, value)

    def test_stats(self):
        for key, value in self.expStats.items():
            out = self.statistics.get(key)
            self.assertEqual(out, value)

