#!/usr/bin/env python
"""
Print shakespeare plays and their sizes.

Use Gutenberg plain versions
"""
import shakespeare.index

def count_words(fileobj):
    """Count the number of words in a file."""
    count = 0 
    for line in fileobj:
        words = line.split()
        count += len(words)
    return count

numtexts = 0
totalwords = 0
for text in shakespeare.index.all:
    # if you wanted the title it would be text.title
    name = text.name
    # want gutenberg version but not folios
    # if you want to include folios remove the second condition
    if '_gut' in name and not '_gut_f' in name:
        numtexts += 1
        fileobj = file(text.get_cache_path('plain'))
        numwords = count_words(fileobj)
        print name.ljust(60), numwords
        totalwords += numwords
print '-------------------------'
print 'Total: %s works, %s words' % (numtexts, totalwords)
