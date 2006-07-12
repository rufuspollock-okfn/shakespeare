import unittest

import StringIO

import shakespeare.textutils

def test_suite():
    suites = [
        unittest.makeSuite(TextUtilsTest),
        ]
    return unittest.TestSuite(suites)

class TextUtilsTest(unittest.TestCase):
    # ['The Phoenix and the Turtle',
    # 'http://www.gutenberg.org/dirs/etext98/cleaned2ws2710.txt', '']
    inStr = \
'''THE PHOENIX AND THE TURTLE

by William Shakespeare




Let the bird of loudest lay,
On the sole Arabian tree,
Herald sad and trumpet be,
To whose sound chaste wings obey.

But thou, shrieking harbinger,
Foul pre-currer of the fiend,
Augur of the fever's end,
To this troop come thou not near.'''

    inFileObj = StringIO.StringIO(inStr)
    
    def test_get_snippet(self):
        exp = '''...Arabian tree,
Herald sad and trumpet be,
To whose sound chaste wing...'''
        # 125 is start of trumpet
        out = shakespeare.textutils.get_snippet(self.inFileObj, 125)
        self.assertEqual(exp, out)
