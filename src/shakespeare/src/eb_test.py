import os

import shakespeare.src.eb as eb
from shakespeare.cache import default as cache

class TestWikimedia:

    def setup_class(self):
        self.wikimedia = eb.Wikimedia()

    def test_make_url(self):
        num = 799
        url = self.wikimedia.make_url(num)
        exp = 'http://upload.wikimedia.org/wikipedia/commons/scans/EB1911_tiff/VOL24%20SAINTE-CLAIRE%20DEVILLE-SHUTTLE/ED4A827.TIF'
        assert url == exp
    
    def test_download(self):
        num = 10 + 772
        self.wikimedia.download(num)
        url = self.wikimedia.make_url(num)
        path = cache.path(url)
        assert os.path.exists(path)

    def test_execute(self):
        "WARNING: this will take a long time the first time it is run ..."
        self.wikimedia.execute()
        url = self.wikimedia.make_url(772)
        path = cache.path(url)
        assert os.path.exists(path)

