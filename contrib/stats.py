#!/usr/bin/env python
import shakespeare.concordance

def print_stats(text_name=None):
    stats = shakespeare.concordance.Statistics(text_name)
    for key in stats.keys():
        print key, stats.get(key)

if __name__ == '__main__':
    import time
    start = time.time()
    print_stats()
    end = time.time()
    print 'Time taken: ', end-start
