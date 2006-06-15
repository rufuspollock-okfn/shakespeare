import os
import urllib

import conf

def get_local_path(remoteUrl, version=''):
    """Get local path to text of remote url.
    @type: string giving version of text (''|'cleaned')
    """
    host,path = urllib.splithost(remoteUrl)
    name = os.path.basename(path)
    name = version + name
    localPath = get_cache_path(name)
    return localPath

def download_url(url, overwrite=False):
    """Download a url to the local cache
    @overwrite: if True overwrite an existing local copy otherwise don't
    """
    localPath = get_local_path(url)
    if overwrite or not(os.path.exists(localPath)):
        urllib.urlretrieve(url, localPath)

def get_cache_path(offset):
    "Get full path of file in cache given by offset."
    return os.path.join(conf.CACHEDIR, offset)

def download_gutenberg_index():
    "Download the Gutenberg Index file GUTINDEX.ALL."
    download_url(conf.GUTINDEX)

