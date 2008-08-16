"""
Statistics for texts.

NB: all word keys have been lower-cased in order to render them
case-insensitive

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
        '''Return word statistics for text, most popular word first.'''
        stats = model.Statistic.query.order_by(model.Statistic.freq.desc()).all()
        return stats

