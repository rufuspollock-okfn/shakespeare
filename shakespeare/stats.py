"""
Statistics for texts.

All word keys are lower-cased in order to render them case-insensitive and
are stemmed using the Xapian standard English stemmer.

TODO
====

1. Provide for normalized statistics (that is occurences normalized by their
occurence in the particular text).

2. Support for aggregate statistics across multiple texts
"""
import re
import xapian

import shakespeare.model as model

class Stats(object):

    @classmethod
    def analyze(self, fileobj):
        '''Get statistics on text in fileobj.

        Words are stemmed so that e.g. love and loved count as the same word.
        '''
        # (?) maybe could use xapian.TermGenerator to split document
        WORD_RE = re.compile('\\w{1,32}', re.U)
        stemmer = xapian.Stem('english')
        results = {}
        text = fileobj.read()
        text = text.decode('utf8', 'ignore')
        text = text.encode('utf8')
        for term in WORD_RE.finditer(text):
            word = term.group()
            word = word.lower()
            stemmed_word = stemmer(word)
            results[stemmed_word] = results.get(stemmed_word, 0) + 1
        return results

    def statsify(self, material, fileobj):
        '''Create statistics associated to domain object `material` whose
        content is in `fileobj`.
        '''
        stats = self.analyze(fileobj)
        for k in stats:
            model.Statistic(text=material,
                    word=k,
                    freq=stats[k]
                    )
        model.Session.flush()

    def freq(self, text, word):
        stat = model.Statistic.query.filter_by(
                text=text).filter_by(word=word).first()
        if stat:
            return stat.freq
        else:
            return 0

    def text_stats(self, text):
        '''Statistics for text, most popular word first.'''
        stats = model.Statistic.query.filter_by(text=text).order_by(
                model.Statistic.freq.desc()
                ).all()
        return stats

    def word_stats(self, word):
        '''Statistics for word (i.e. which texts use it) in order or
        usage.'''
        stats = model.Statistic.query.filter_by(word=word).order_by(
                model.Statistic.freq.desc()
                ).all()
        return stats

