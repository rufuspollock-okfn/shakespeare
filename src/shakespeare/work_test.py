import unittest
import shakespeare.work

def test_suite():
    suites = [
        unittest.makeSuite(GutenbergIndexTest),
        unittest.makeSuite(ShakespeareIndexTest),
    ]
    return unittest.TestSuite(suites)

class GutenbergIndexTest(unittest.TestCase):

    def setUp(self):
        self.gutindex = shakespeare.work.GutenbergIndex()
    
    def test_parse_line_for_folio(self):
        inStr = 'Jul 2000 Cymbeline, by Wm. Shakespeare  [First Folio]=[FF] [0ws39xxx.xxx] 2269'
        out = self.gutindex.parse_line_for_folio(inStr)
        exp = ['Cymbeline', '2000', '0ws39']
        for ii in range(len(exp)):
            self.assertEqual(out[ii], exp[ii])
    
    def test_parse_line_for_normal(self):
        inStr = 'Nov 1998 Cymbeline, by William Shakespeare [2ws39xxx.xxx] 1538'
        out = self.gutindex.parse_line_for_normal(inStr)
        exp = ['Cymbeline', '1998', '2ws39']
        for ii in range(len(exp)):
            self.assertEqual(out[ii], exp[ii])
    
    def test_make_url(self):
        exp = 'http://www.gutenberg.org/dirs/etext00/0ws3910.txt'
        out = self.gutindex.make_url('2000', '0ws39')
        self.assertEqual(exp, out)
    
    def test_make_url_2(self):
        exp = 'http://www.gutenberg.org/dirs/etext98/2ws3910.txt'
        out = self.gutindex.make_url('1998', '2ws39')
        self.assertEqual(exp, out)
    
    def test__extract_shakespeare_works(self):
        plays = self.gutindex._extract_shakespeare_works()
        self.assertEqual(len(plays), 73)

#    def test_get_etext_url(self):
#        number = 11125
#        exp = 'http://www.gutenberg.org/dirs/1/1/1/2/11125/11125.txt'
#        out = get_etext_url(number)
#        self.assertEqual(out, exp)

class ShakespeareIndexTest(unittest.TestCase):
    def setUp(self):
        self.index = shakespeare.work.index

    def test_get_all(self):
        all = self.index.all
        self.assertEqual(len(all), 74)
 
