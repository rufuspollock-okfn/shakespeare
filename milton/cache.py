import os
import urllib

import milton
conf = milton.conf()

class Cache(object):
    """Provide a local filesystem cache for material.
    """

    def __init__(self, cache_path):
        self.cache_path = cache_path

    def path(self, remote_url, version=''):
        """Get local path to text of remote url.
        @type: string giving version of text (''|'cleaned')
        """
        protocolEnd = remote_url.index(':') + 3  # add 3 for ://
        path = remote_url[protocolEnd:]
        base, name = os.path.split(path)
        name = version + name
        offset = os.path.join(base, name)
        localPath = self.path_from_offset(offset)
        return localPath

    def download_url(self, url, overwrite=False):
        """Download a url to the local cache
        @overwrite: if True overwrite an existing local copy otherwise don't
        """
        localPath = self.path(url)
        dirpath = os.path.dirname(localPath)
        if overwrite or not(os.path.exists(localPath)):
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            # use wget as it seems to work more reliably on wikimedia
            # rgrp: 2008-03-18 use urllib rather than wget despite these issues
            # as wget is fairly specific to linux/unix and even there may not
            # be installed.
            # cmd = 'wget -O %s %s' % (localPath, url) 
            # os.system(cmd)
            urllib.urlretrieve(url, localPath)

    def path_from_offset(self, offset):
        "Get full path of file in cache given by offset."
        return os.path.join(self.cache_path, offset)


default_path = milton.conf()['cachedir']
default = Cache(default_path)

