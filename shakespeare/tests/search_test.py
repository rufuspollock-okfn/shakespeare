import os
import shutil
import tempfile
import StringIO

import shakespeare.search

class TestSearch:
    # break up a little to make indexing more interesting
    text = \
'''
Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:

Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd,
And every fair from fair sometime declines,
By chance, or nature's changing course untrimm'd: 

But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st,
Nor shall death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st,

  So long as men can breathe, or eyes can see,
  So long lives this, and this gives life to thee.
'''

    def setUp(self):
        basetmp = tempfile.gettempdir()
        self.tmpdir = os.path.join(basetmp, 'openshkspr-search')
        # we leave directory in existence to help with debugging
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        self.index = shakespeare.search.SearchIndex(self.tmpdir)

    def test_add_item(self):
        self.index.add_item(StringIO.StringIO(self.text))

    def test_search(self):
        self.index.add_item(StringIO.StringIO(self.text))
        out = self.index.search('summer')
        assert len(out) == 2
        out = self.index.search('rough')
        assert len(out) == 1

