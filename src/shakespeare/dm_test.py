import unittest

import shakespeare.dm

def test_suite():
    suites = [
        unittest.makeSuite(WorkTextTest),
        unittest.makeSuite(ConcordanceTest),
        ]
    return unittest.TestSuite(suites)

shakespeare.dm.rebuilddb()

class WorkTextTest(unittest.TestCase):
    
    def test1(self):
        name = 'hamlet_1'
        title = 'Hamlet'
        txt = shakespeare.dm.WorkText(title=title, name=name)
        txtid = txt.id
        txt2 = shakespeare.dm.WorkText.get(txtid)
        txt3 = shakespeare.dm.WorkText.byName(name)
        self.assertEqual(txt.id, txt2.id)
        self.assertEqual(txt.id, txt3.id)

class ConcordanceTest(unittest.TestCase):
    
    def test_get_snippet(self):
        pass
