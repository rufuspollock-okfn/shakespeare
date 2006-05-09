import re
import cPickle

import utils
import shakespeare.work

def make_concordancer(
        texts_to_add=shakespeare.work.index.all,
        out_path=utils.get_local_path('concordance.p'),
        ):
    """Create Concordancer object and use it to produce concordance and stats
    for all non-folio works.
    @out_path: where to save the concordance
    @texts_to_add: index items that should be added to the concordance
    """
    cc = Concordancer()
    for item in texts_to_add:
        url = item[1]
        isfolio = item[2] == 'folio'
        src = utils.get_local_path(url, 'cleaned')
        cc.add_text(file(src))
    ccFile = file(out_path, 'w')
    cPickle.dump(cc, ccFile)

def get_concordancer():
    """Get a concordancer containing concordance and stats by unpickling cached
    copy.
    """
    filePath = utils.get_local_path('concordance.p')
    cc = cPickle.load(file(filePath))
    return cc

class Concordancer(object):
    """Generate a concordance and associated statistics for a set of texts.
    
    Concordance and statistics are provided as dictionaries keyed by words.
    NB: all word keys have been lower-cased in order to render them case-insensitive
    """

    # multiline, unicode and ignorecase
    word_regex = re.compile(r'\b(\w+)\b', re.U | re.M | re.I)

    words_to_ignore = [ 'a', 'the', 'and',
                        'as', 'are', 'be',
                        'but', 'd', 'in'
                        ]

    def __init__(self):
        self.concordance = {}
        self.stats = {}

    def add_text(self, text, textId=None):
        """Add a text to the concordance.
        @text: file like object containing text to add
        """
        lineCount = 0
        charIndex = 0
        for line in text.readlines():
            for match in self.word_regex.finditer(line):
                word = match.group().lower() # case insensitive
                if word in self.words_to_ignore:
                    continue
                oldValue = self.concordance.get(word, [])
                oldStat = self.stats.get(word, 0)
                tloc = (textId, lineCount, charIndex + match.start()) 
                oldValue.append(tloc)
                self.concordance[word] = oldValue
                self.stats[word] = oldStat + 1
            lineCount += 1
            charIndex += len(line)

