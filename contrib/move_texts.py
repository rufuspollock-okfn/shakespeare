# move data from cache to shksprdata
import os
import shutil

import shakespeare.index
ourindex = shakespeare.index.all

store = './shksprdata/texts'

if not os.path.exists(store):
    os.makedirs(store)

meta_path = os.path.join(store, 'metadata.txt')
from ConfigParser import SafeConfigParser
cfp = SafeConfigParser()
# might want to support re-running ...
cfp.read(meta_path)

# texts that still need cleaning: winters_tale_gut

for row in ourindex:
    if not 'moby' in row.name:
        path = row.get_cache_path(format='plain') 
        name = row.name
        # these are all plain txt
        newpath = os.path.join(store, name + '.txt')
        print 'Moving %s to %s' % (path, newpath)
        src = file(path)
        dest = file(newpath, 'w')
        dest.write(src.read())
        dest.close()
        src.close()
        if not cfp.has_section(name):
            cfp.add_section(name)
            cfp.set(name, 'title', row.title)
            cfp.set(name, 'notes', row.notes)
            cfp.set(name, 'format', 'txt')
            cfp.set(name, 'creator', row.creator)
            cfp.set(name, 'url', row.url)

cfp.write(file(meta_path, 'w'))
