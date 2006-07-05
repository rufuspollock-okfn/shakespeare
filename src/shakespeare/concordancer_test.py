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
    textId = 1
    
    # ['work_id', 'line-no', 'character-index'] }
    expConcordance = {
        'fake' : [ (textId, 0, 2), (textId, 0, 7) ],
        'suffolk' : [ (textId, 1, 17), ],
        'high' : [ (textId, 2, 37), ],
        }

    expStats = {
        'fake' : 2,
        'suffolk' : 1,
        'high' : 1,
        }

    def setUp(self):
        self.cc = shakespeare.concordancer.Concordancer()
        self.cc.add_text(StringIO.StringIO(self.inText), self.textId)

    def test__process_line(self):
        line = 'the - quick, brown. fox-jumped over$ the_lazy do8g.'
        exp = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the_lazy', 'do8g' ]
        out = self.cc.word_regex.findall(line)
        self.assertEqual(exp, out)

    def test_concordance(self):
        for key, value in self.expConcordance.items():
            out = self.cc.concordance[key]
            self.assertEqual(out, value)

    def test_stats(self):
        for key, value in self.expStats.items():
            out = self.cc.stats[key]
            self.assertEqual(out, value)

    def test_make_concordancer(self):
        filePath = tempfile.mkstemp()[1]
        index = shakespeare.index.all
        shakespeare.concordancer.make_concordancer(index[2:3], filePath)
