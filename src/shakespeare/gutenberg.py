"""Various useful functionality related to Project Gutenberg
"""
import os

import shakespeare.utils as utils

class GutenbergIndex(object):
    """Parse the index of Gutenberg works so as to find Shakespeare works.
    TODO: Gutenberg now make available the index in RDF/XML form:
      http://www.gutenberg.org/feeds/catalog.rdf.bz2
    and we should try to use that instead of plain text file
    """
    
    # url for the Gutenberg index file
    gutindex = 'http://www.gutenberg.org/dirs/GUTINDEX.ALL'

    def __init__(self):
        self.download_gutenberg_index()
        self._gutindex_local_path = utils.get_local_path(self.gutindex)

    def download_gutenberg_index(self):
        """Download the Gutenberg Index file GUTINDEX.ALL to cache if we don't
        have it already.
        """
        utils.download_url(self.gutindex)

    def make_url(self, year, idStr):
        return 'http://www.gutenberg.org/dirs/etext%s/%s10.txt' % (year[2:], idStr)

    def get_shakespeare_list(self):
        """Get list of shakespeare works and urls.
        Results are sorted by work title.
        """
        # results have format [ title, url, comments ]
        # folio in comments indicates it is a first folio
        results = [ ["Sonnets", 'http://www.gutenberg.org/dirs/etext97/wssnt10.txt', ''] ]
        plays = self._extract_shakespeare_works()
        for play in plays:
            url = self.make_url(play[1], play[2])
            results.append([play[0], url, play[3]])
        def compare_list(item1, item2):
            if item1[0] > item2[0]: return 1
            else: return -1
        results.sort(compare_list)
        return results
    
    def _extract_shakespeare_works(self):
        """Get non-copyrighted Shakespeare works from Gutenberg
        Results consist of folio and one other 'standard' version.
        @return: list consisting of tuples in form [title, year, id, comment]
        """
        ff = file(self._gutindex_local_path)
        results = []
        for line in ff.readlines():
            result = self.parse_line_for_folio(line)
            if result:
                results.append(result + ['folio'])
            resultNormal = self.parse_line_for_normal(line)
            if resultNormal:
                results.append(resultNormal + [''])
        return results
    
    def parse_line_for_normal(self, line):
        "Parse GUTINDEX line for the 'normal' gutenberg shakespeare versions (i.e. not folio and out of copyright)."
        if 'by William Shakespeare' in line and '[2' in line:
            year = line[4:8]
            tmp = line[9:]
            endOfTitle = tmp.find(', by')
            title = tmp[:endOfTitle]
            startOfId = tmp.find('[2')
            endOfId = tmp.find(']', startOfId)
            idStr = tmp[startOfId+1:endOfId]
            xstart = idStr.find('x')
            idStr = idStr[:xstart]
            return [title, year, idStr]
        
    def parse_line_for_folio(self, line):
        if '[FF]' in line:
            year = line[4:8]
            tmp = line[9:]
            endOfTitle = tmp.find(', by')
            title = tmp[:endOfTitle]
            startOfId = tmp.find('[FF]') + 5
            endOfId = tmp.find(']', startOfId)
            idStr = tmp[startOfId+1:endOfId]
            xstart = idStr.find('x')
            idStr = idStr[:xstart]
            return [title, year, idStr]
        else:
            return None


"""
Clean up Gutenberg texts by removing all the header and footer bumpf
"""

import re

headerEndPhrases = ["Project Gutenberg's Etext of", 'This etext was prepared by']
notesStartPhrases = ["Executive Director's Notes:"]
notesEndPhrases = ['David Reed']
footerStartPhrases = ['End of Project Gutenberg', 'End of The Project Gutenberg'
    ]

def make_re_from_phrase(phrase):
    """
    Make a regular expression that matches a phrase and its surrounding
    paragraph, i.e. that look like:
    
    ... phrase ....
    more text
    [blank]
    [blank]+
    """
    paragraphText = '(.+\S.+\n)*' # need \S to ensure not just whitespace
    # [[TODO: check slowdown due to inclusion of '^.*' at start
    tmp = '^.*' + phrase + '.*\n' + paragraphText + '\s+'
    return re.compile(tmp, re.I | re.M)  # make it case insensitive

class GutenbergShakespeare(object):
    """
    Process Gutenberg shakespeare texts
    """
    
    def __init__(self, etext):
        """
        @param etext: file like object containing the etext
        
        Procedure:
            1. strip out header and footer bumpf
            2. are there notes? If so strip them out
        """
        self.etext = etext
        self.etextStr = self.etext.read()
        # normalize the line endings to save us grief later
        self.etextStr = self.etextStr.replace('\r\n', '\n')
        self.hasNotes = False
    
    def _find_max(self, phrase, string):
        maxIndex = 0
        regex = make_re_from_phrase(phrase)
        matches = regex.finditer(string)
        for match in matches:
            maxIndex = max(match.end(), maxIndex)
        return maxIndex
    
    def _find_min(self, phrase, string):
        minIndex = len(string)
        regex = make_re_from_phrase(phrase)
        matches = regex.finditer(string)
        for match in matches:
            minIndex = min(match.start(), minIndex)
        return minIndex
    
    def extract_text(self):
        """Extract the core text.
        """
        self.notesEnd = self.get_notes_end()
        self.headerEnd = self.get_header_end()
        self.footerStart = self.get_footer_start()
        startIndex = self.headerEnd
        if self.notesEnd > 0:
            startIndex = self.notesEnd
        return self.etextStr[startIndex : self.footerStart].rstrip()
        
    def get_notes_end(self):
        "Return 0 if no notes"
        indices = [ self._find_max(phrase, self.etextStr) for phrase in notesEndPhrases]
        index = max(indices)
        return index
    
    def get_header_end(self):
        indices = [ self._find_max(phrase, self.etextStr) for phrase in headerEndPhrases]
        return max(indices)
    
    def get_footer_start(self):
        indices = [ self._find_min(phrase, self.etextStr) for phrase in footerStartPhrases]
        return min(indices)


class ShakespeareIndex(object):

    def __init__(self):
        gutindex = GutenbergIndex()
        self.all = gutindex.get_shakespeare_list()
        # todo: parse it up
        self.folios = None
        self.nonfolios = None
        self.sonnets = None

#def get_etext_url(number):
#    """
#    [[TODO: DOES NOT WORK]]
#    Get the url for an etext given its number.
#    This is non-trivial and follows instructions at start of GUTINDEX.ALL
#    """
#    baseUrl = 'http://www.gutenberg.org/dirs/'
#    ss = ''
#    if number > 10000:
#        ss = str(number)
#        for char in ss[:-1]:
#            pass
#    if number <= 10000:
#        raise 'Cannot deal with etext numbers less than 10000'
#    return ss
