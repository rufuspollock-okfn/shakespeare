#!/usr/bin/env python
import sys

import shakespeare.dm

name = sys.argv[1]
work = shakespeare.dm.Material.byName(name)
path = work.get_text()
ff = file(path)
print path
indata = unicode(ff.read(), 'utf-8')
print indata.encode('utf-8')
