import unittest

import shakespeare.dm

def test_suite():
    suites = [
        unittest.makeSuite(MaterialTest),
        unittest.makeSuite(ConcordanceTest),
        ]
    return unittest.TestSuite(suites)

shakespeare.dm.rebuilddb()


class MaterialTest(unittest.TestCase):

    def setUp(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = shakespeare.dm.Material(name=self.name, title=self.title)

    def tearDown(self):
        shakespeare.dm.Material.delete(self.text.id)
    
    def test1(self):
        txtid = self.text.id
        txt2 = shakespeare.dm.Material.get(txtid)
        txt3 = shakespeare.dm.Material.byName(self.name)
        self.assertEqual(self.text.id, txt2.id)
        self.assertEqual(self.text.id, txt3.id)

class ConcordanceTest(unittest.TestCase):

    def setUp(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = shakespeare.dm.Material(name=self.name, title=self.title)

    def tearDown(self):
        shakespeare.dm.Material.delete(self.text.id)

    def test1(self):
        word = 'jones'
        line = 20
        char_index = 500
        cc1 = shakespeare.dm.Concordance(text=self.text,
                                         word=word,
                                         line=line,
                                         char_index=char_index)
        out1 = shakespeare.dm.Concordance.get(cc1.id)
        self.assertEqual(self.text, out1.text)

