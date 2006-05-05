import re
import cPickle

import utils
from download import make_index

def make_concordancer(showProgress=True):
    """Create Concordancer object and use it to produce concordance and stats
    for all non-folio works.
    Save resulting object in pickled form to 'concordance.p'.
    """
    def _print(msg):
        if showProgress:
            print(msg)
    index = make_index()
    cc = Concordancer()
    for item in index:
        url = item[1]
        isfolio = item[2] == 'folio'
        src = utils.get_local_path(url, 'cleaned')
        if isfolio:
            _print('Is folio so skipping [%s]' % src)
        else:
            _print('Adding text [%s]' % src)
            cc.add_text(file(src))
    filePath = utils.get_local_path('concordance.p')
    ccFile = file(filePath, 'w')
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
    wordRegex = re.compile(r'\b(\w+)\b', re.U | re.M | re.I)

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
            for match in self.wordRegex.finditer(line):
                word = match.group().lower() # case insensitive
                oldValue = self.concordance.get(word, [])
                oldStat = self.stats.get(word, 0)
                oldValue.append( (lineCount, charIndex + match.start()) )
                self.concordance[word] = oldValue
                self.stats[word] = oldStat + 1
            lineCount += 1
            charIndex += len(line)


