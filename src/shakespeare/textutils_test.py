import unittest

import textutils

def test_suite():
    suites = [
        unittest.makeSuite(TextUtilsTest),
        ]
    return unittest.TestSuite(suites)

class TextUtilsTest(unittest.TestCase):
    # ['The Phoenix and the Turtle',
    # 'http://www.gutenberg.org/dirs/etext98/cleaned2ws2710.txt', '']
    textUrl = 'http://www.gutenberg.org/dirs/etext98/2ws2710.txt'
    
    def test_get_snippet(self):
        exp = '''...Arabian tree,
Herald sad and trumpet be,
To whose sound chaste wing...'''
        # 125 is start of trumpet
        out = textutils.get_snippet(self.textUrl, 125)
        self.assertEqual(exp, out)
