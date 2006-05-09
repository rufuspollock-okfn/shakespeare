import unittest

import utils
from format import make_re_from_phrase, GutenbergShakespeare 

def test_suite():
    suites = [
        unittest.makeSuite(FormatTest),
        unittest.makeSuite(GutenbergShakespeareTest),
        ]
    return unittest.TestSuite(suites)

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
    etext1 = file(utils.get_cache_path('0ws2510.txt'))
    etext2 = file(utils.get_cache_path('2ws2510.txt'))
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

