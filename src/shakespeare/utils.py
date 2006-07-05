import os
import urllib

import shakespeare
conf = shakespeare.conf()

def get_local_path(remoteUrl, version=''):
    """Get local path to text of remote url.
    @type: string giving version of text (''|'cleaned')
    """
    protocolEnd = remoteUrl.index(':') + 3  # add 3 for ://
    path = remoteUrl[protocolEnd:]
    base, name = os.path.split(path)
    name = version + name
    offset = os.path.join(base, name)
    localPath = get_cache_path(offset)
    return localPath

def download_url(url, overwrite=False):
    """Download a url to the local cache
    @overwrite: if True overwrite an existing local copy otherwise don't
    """
    localPath = get_local_path(url)
    dirpath = os.path.dirname(localPath)
    if overwrite or not(os.path.exists(localPath)):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        urllib.urlretrieve(url, localPath)

def get_cache_path(offset):
    "Get full path of file in cache given by offset."
    cachedir = conf.get('misc', 'cachedir')
    return os.path.join(cachedir, offset)

