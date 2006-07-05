import unittest
import shakespeare.gutenberg
import shakespeare.utils as utils
from shakespeare.gutenberg import make_re_from_phrase, GutenbergShakespeare 

def test_suite():
    suites = [
        unittest.makeSuite(GutenbergIndexTest),
        unittest.makeSuite(FormatTest),
        unittest.makeSuite(GutenbergShakespeareTest),
    ]
    return unittest.TestSuite(suites)


class GutenbergIndexTest(unittest.TestCase):

    def setUp(self):
        self.gutindex = shakespeare.gutenberg.GutenbergIndex()
    
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


class FormatTest(unittest.TestCase):
    
    def test_make_re_from_phrase(self):
        outStr = """blah
            
            
            """
        inStr = outStr + 'All is Well that'
        regex = make_re_from_phrase('blah')
        out = regex.search(inStr)
        self.assertEquals(out.group(), outStr)
    
    def test_makeReFromPhrase2(self):
        outStr = """blah
            joe
            hello
            
            
            """
        inStr = outStr + 'All is Well that'
        regex = make_re_from_phrase('blah')
        out = regex.search(inStr)
        self.assertEquals(out.group(), outStr)

class GutenbergShakespeareTest(unittest.TestCase):
    # As you like it in Folio and normal
    url1 = 'http://www.gutenberg.org/dirs/etext00/0ws2510.txt'
    url2 = 'http://www.gutenberg.org/dirs/etext98/2ws2510.txt'
    utils.download_url(url1)
    utils.download_url(url2)
    etext1 = file(utils.get_local_path(url1))
    etext2 = file(utils.get_local_path(url2))
    gut1 = GutenbergShakespeare(etext1)
    gut2 = GutenbergShakespeare(etext2)
    
    def test_get_header_end(self):
        out = self.gut1.get_header_end()
        exp = self.gut1.etextStr.index("Executive Director's Notes:")
        self.assertEqual(out, exp)
    
    def test_get_footer_start(self):
        out = self.gut1.get_footer_start()
        # has no footer 
        exp = len(self.gut1.etextStr)
        self.assertEqual(out, exp)
        
        out = self.gut2.get_footer_start()
        exp = self.gut2.etextStr.index("End of Project Gutenberg Etext of As You Like It by Shakespeare")
        self.assertEqual(out, exp)
    
    def test_get_notes_end(self):
        out = self.gut1.get_notes_end()
        exp = self.gut1.etextStr.index("As you Like it\n\nActus")
        self.assertEqual(out, exp)

    def test_extract_text(self):
        # [[TODO: run this test on all of the etexts]]
        for gut in [self.gut1, self.gut2]:
            out = gut.extract_text()
            notFound = (out.find('Gutenberg') == -1)
            self.failUnless(notFound)

#    def test_get_etext_url(self):
#        number = 11125
#        exp = 'http://www.gutenberg.org/dirs/1/1/1/2/11125/11125.txt'
#        out = get_etext_url(number)
#        self.assertEqual(out, exp)

