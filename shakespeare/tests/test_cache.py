import os
import shutil
import tempfile

import shakespeare.cache

class TestCache(object):

    @classmethod
    def setup_class(cls):
        cls.cache_path = tempfile.mkdtemp()
        cls.cache = shakespeare.cache.Cache(cls.cache_path)
        cls.url = 'http://www.gutenberg.org/dirs/GUTINDEX.ALL'
        cls.url2 = 'http://project.knowledgeforge.net/shakespeare/svn/trunk/CHANGELOG.txt'

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.cache_path)

    def test_path(self):
        exp = os.path.join(self.cache_path, self.url[7:])
        out = self.cache.path(self.url)
        assert out == exp, (out, exp)

    def test_path_2(self):
        exp = os.path.join(self.cache_path,
                'www.gutenberg.org/dirs/cleanedGUTINDEX.ALL')
        out = self.cache.path(self.url, 'cleaned')
        assert exp == out

    def test_path_without_fullpath(self):
        cache2 = shakespeare.cache.Cache('', fullpath=False)
        out = cache2.path(self.url)
        assert out == 'GUTINDEX.ALL'

    def test_download_url(self):
        exp = os.path.join(self.cache_path, self.url2[7:])
        self.cache.download_url(self.url2, overwrite=True)
        assert os.path.exists(exp)
 
