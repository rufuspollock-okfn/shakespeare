#!/usr/bin/env python
import shakespeare.concordance
import profile
import pstats

outfile = 'profiler_results.txt'

def foo():
    # cc = shakespeare.concordance.Concordance()
    stats = shakespeare.concordance.Statistics()
    words = stats.keys()

def dosel():
    sqlcc = shakespeare.dm.Concordance
    out = sqlcc.select()
    return out

def dostuff(results):
    words = []
    count = 0
    for xx in results:
        count += 1
        if count >= 200: break
    print count
    # words = [ xx.word for xx in all ]
    # distinct = list(set(words))
    # distinct.sort()

def foo2():
    all = dosel()
    dostuff(all)

def run_profiler():
    profile.run('foo()', outfile)

def analyse():
    stats = pstats.Stats(outfile)
    # stats.sort_stats('cumulative').print_stats()
    stats.sort_stats('time').print_stats()

if __name__ == '__main__':
    run_profiler()
    analyse()
