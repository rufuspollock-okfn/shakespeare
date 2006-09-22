import shakespeare.index

class TestShakespeareIndex:

    index = shakespeare.index.ShakespeareIndex()

    def test_get_all(self):
        all = list(self.index.all)
        # not possible to know how many are in there
        # expNumRecs = 0
        # self.assertEqual(expNumRecs, len(all))
 
