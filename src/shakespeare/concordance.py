"""
Concordance (and statistics) for texts in database.

To build concordance use ConcordanceBuilder.  To access concordance/statistics
use Concordance/Statistics class.  Concordance and statistics are provided as
dictionaries keyed by words.

NB: all word keys have been lower-cased in order to render them
case-insensitive
"""
import re

import utils
import shakespeare.index

import sqlobject

class ConcordanceBase(object):
    """
    TODO: caching??
    """
    sqlcc = shakespeare.dm.Concordance

    def __init__(self, filter_names=None):
        """
        @param filter_names: a list of id names with which to filter results
            (i.e. only return results relating to those texts)
        """
        self._filter_names = filter_names
        # piece of sql to use in select to filter texts
        self._sql_filter = True
        if self._filter_names is not None:
            arglist = []
            for name in self._filter_names:
                newarg = self.sqlcc.q.textID == self._name2id(name)
                arglist.append(newarg)
            self._sql_filter = sqlobject.OR(*arglist)
    
    def _name2id(self, name):
        return shakespeare.dm.Material.byName(name).id

    def keys(self):
        """Return list of words in concordance
        """
        # distinct does not help us because we need to DISTINCT word
        # but can't do this with sqlobject
        all = self.sqlcc.select(self._sql_filter,
                           orderBy=self.sqlcc.q.word,
                           distinct=True)
        words = [ xx.word for xx in list(all) ]
        distinct = list(set(words))
        distinct.sort()
        return distinct


class Concordance(ConcordanceBase):
    """Concordance by word for a set of texts
    """

    def get(self, word):
        """Get list of occurrences for word
        @return: sqlobject query list 
        """
        select = self.sqlcc.select(sqlobject.AND(self._sql_filter, self.sqlcc.q.word==word))
        return select

class Statistics(ConcordanceBase):

    def get(self, word):
        select = self.sqlcc.select(
            sqlobject.AND(self._sql_filter, self.sqlcc.q.word==word)
            )
        return select.count()

class ConcordanceBuilder(object):
    """Build a concordance and associated statistics for a set of texts.
    
    """

    # multiline, unicode and ignorecase
    word_regex = re.compile(r'\b(\w+)\b', re.U | re.M | re.I)

    words_to_ignore = [ 
        # 'a', 'the', 'and', 'as', 'are', 'be', 'but', 'd', 'in'
                        ]

    def _text_already_done(self, text):
        numrecs = shakespeare.dm.Concordance.select(
                shakespeare.dm.Concordance.q.textID==text.id
                ).count()
        return numrecs > 0

    def add_text(self, name, text=None):
        """Add a text to the concordance.
        @param name: name of text to add
        @param text: [optional] a file-like object containing text data. If not
            provided will default to using file in cache associated with named
            text
        """
        dmText = shakespeare.dm.Material.byName(name)
        if self._text_already_done(dmText):
            msg = 'Have already added to concordance text: %s' % dmText
            # raise ValueError(msg)
            print msg
            print 'Skipping'
            return
        if text is None:
            text = file(dmText.cache_path)
        lineCount = 0
        charIndex = 0
        for line in text.readlines():
            for match in self.word_regex.finditer(line):
                word = match.group().lower() # case insensitive
                if word in self.words_to_ignore:
                    continue
                shakespeare.dm.Concordance(text=dmText,
                                           word=word,
                                           line=lineCount,
                                           char_index=charIndex+match.start())
            lineCount += 1
            charIndex += len(line)

    def remove_text(self, name):
        """Remove a text from the concordance.

        @param name: as for add_text
        """
        dmText = shakespeare.dm.Material.byName(name)
        recs = shakespeare.dm.Concordance.select(
                shakespeare.dm.Concordance.q.textID==dmText.id
                )
        for rec in recs:
            shakespeare.dm.Concordance.delete(rec.id)

