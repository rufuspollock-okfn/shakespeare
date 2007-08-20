"""Encylopaedia Britannica (11th ed) material.
"""
from shakespeare.cache import default as cache
import os
import time

class Wikimedia(object):
    """Extract EB shakespeare related material from wikimedia.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

    def execute(self):
        "Do the work."
        # 28 pages starting at 772
        for ii in range(28):
            pagenum = 772 + ii
            self.download(pagenum)

    def download(self, page_number):
        url = self.make_url(page_number)
        if self.verbose:
            print 'Downloading: ', url
        # problems with incomplete downloads from wikimedia for some files when
        # using urllib.urlretrieve (d/l works from a browser or wget)
        # investigation showed we were getting stuff like for the problem files
        # X-Squid-Error: ERR_ACCESS_DENIED 0
        def download_success(url):
            # these are pretty large files
            expected_min_file_size = 100000
            local_path = cache.path(url)
            out = (os.path.exists(local_path)
                    and os.stat(local_path).st_size > expected_min_file_size
                    )
            return out
        cache.download_url(url)
        if not download_success(url):
            print 'ERROR: failed to download %s successfully' % url

    def make_url(self, page_number):
        """Generate urls for wikimedia diffs.

        @param page_number: EB page number you want from volume 24.

        """
        base_path = 'http://upload.wikimedia.org/wikipedia/commons/scans/EB1911_tiff/'
        volume = 'VOL24%20SAINTE-CLAIRE%20DEVILLE-SHUTTLE/'
        # wikimedia page numbers are +28 compared to EB numbers.
        urlnum = page_number + 28
        urlnum = str(urlnum)
        fn = 'ED4A' + urlnum + '.TIF'
        return base_path + volume + fn 

