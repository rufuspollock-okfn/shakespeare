import os
import urlparse
import urllib

class Cache(object):
    """Provide a local filesystem cache for material.
    """

    def __init__(self, cache_path, fullpath=True):
        '''
        @param fullpath: save to local path corresponding to full url path
            (creating directories as necessary) when retrieving.
        '''
        self.cache_path = cache_path
        self.fullpath = fullpath

    def path(self, remote_url, version=''):
        """Get local path to text of remote url.
        @type: string giving version of text (''|'cleaned')
        """
        urlparts = urlparse.urlparse(remote_url)
        base = urlparts[1]
        pathparts = urlparts[2].split('/')
        if len(pathparts) > 1:
            base = os.path.join(base, *pathparts[:-1])
        name = pathparts[-1]
        name = version + name
        if self.fullpath:
            offset = os.path.join(base, name)
        else:
            offset = name
        local_path = self.path_from_offset(offset)
        return local_path

    def path_from_offset(self, offset):
        "Get full path of file in cache given by offset."
        if offset.startswith('/'):
            offset = offset[1:]
        return os.path.join(self.cache_path, offset)

    def save(self, path, data):
        fp = self.path_from_offset(path)
        fo = open(fp, 'w')
        fo.write(data)
        fo.close()

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
            # see extensive comments on issue in shakespeare.eb.Wikimedia class
            # rgrp: 2008-03-18 use urllib rather than wget despite these issues
            # as wget is fairly specific to linux/unix and even there may not
            # be installed.
            # cmd = 'wget -O %s %s' % (localPath, url) 
            # os.system(cmd)
            urllib.urlretrieve(url, localPath)


try:
    import shakespeare
    conf = shakespeare.conf()

    default_path = shakespeare.conf()['cachedir']
    default = Cache(default_path)
except:
    pass

