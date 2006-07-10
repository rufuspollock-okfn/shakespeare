import unittest

import shakespeare.index

def test_suite():
    suites = [
        unittest.makeSuite(ShakespeareIndexTest),
    ]
    return unittest.TestSuite(suites)


class ShakespeareIndexTest(unittest.TestCase):

    def setUp(self):
        self.index = shakespeare.index.ShakespeareIndex()

    def test_get_all(self):
        all = list(self.index.all)
        self.assertEqual(len(all), 0)
 
