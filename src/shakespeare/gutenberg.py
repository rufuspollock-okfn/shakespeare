"""Various useful functionality related to Project Gutenberg
"""
import os
import StringIO
import shakespeare.utils


class GutenbergIndex(object):
    """Parse the index of Gutenberg works so as to find Shakespeare works.

    TODO: Gutenberg now make available the index in RDF/XML form:
    http://www.gutenberg.org/feeds/catalog.rdf.bz2 and we should try to use
    that instead of plain text file
    """
    
    # url for the Gutenberg index file
    gutindex = 'http://www.gutenberg.org/dirs/GUTINDEX.ALL'

    def __init__(self):
        self.download_gutenberg_index()
        self._gutindex_local_path = shakespeare.utils.get_local_path(self.gutindex)

    def download_gutenberg_index(self):
        """Download the Gutenberg Index file GUTINDEX.ALL to cache if we don't
        have it already.
        """
        shakespeare.utils.download_url(self.gutindex)

    def make_url(self, year, idStr):
        return 'http://www.gutenberg.org/dirs/etext%s/%s10.txt' % (year[2:], idStr)

    def get_shakespeare_list(self):
        """Get list of shakespeare works and urls.

        Results are sorted by work title.

        Notes regarding list of plays:

          * no Folio edition of Troilus and Cressida
          * no Folio edition of Pericles
        """
        # results have format [ title, url, comments ]
        # folio in comments indicates it is a first folio
        results = [ ["Sonnets", 'http://www.gutenberg.org/dirs/etext97/wssnt10.txt', ''] ]
        plays = self._extract_shakespeare_works()
        for play in plays:
            url = self.make_url(play[1], play[2])
            results.append([play[0], url, play[3]])
        # add in by hand some exceptions
        results.append(["The Winter's Tale",
                'http://www.gutenberg.org/files/1539/1539.txt', '']
                )
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
        """Parse GUTINDEX for 'normal' gutenberg shakespeare versions (i.e. not
        folio and out of copyright).
        """
        # normal shakespeare are those with id starting [2
        # most have 'by William Shakespeare' but also have 'by Shakespeare'
        # (Othello) and 'by Wm Shakespeare' (Titus Andronicus)
        # everything is by William Shakespeare except for Othello
        if ('Shakespeare' in line and '[2' in line
                and 'mp3' not in line and 'Apocrypha' not in line):
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


class Helper(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        gutindex = GutenbergIndex()
        self._index = gutindex.get_shakespeare_list()
     
    def _filter_index(self, line):
        """Filter items in index return only those whose id (url) is in line.
        If line is empty or None return all items
        """
        if line:
            textsToAdd = []
            textsUrls = line.split()
            for item in self._index:
                if item[1] in textsUrls:
                    textsToAdd.append(item)
            return textsToAdd
        else:
            return self._index
    
    def get_index(self, line=None):
        """Get list of texts
        """
        return self._index

    def download(self, line=None):
        """Download from Project Gutenberg all the shakespeare texts listed in the
        index.
        """
        for item in self._index:
            title = item[0]
            url = item[1]
            if self.verbose:
                print 'Downloading %s (%s)' % (url, title)
            shakespeare.utils.download_url(item[1])
    
    def clean(self, line=None):
        """Clean up raw gutenberg texts to extract underlying work (so remove
        all extra bumpf such as Gutenberg licence, contributor info etc).
        
        Texts are written to same directory as original file with 'cleaned'
        prepended to their name.
        
        @param line: space separated list of text urls: text-url text-url
        """
        textsToProcess = self._filter_index(line) 
        for item in textsToProcess:
            url = item[1]
            src = shakespeare.utils.get_local_path(url)
            dest = shakespeare.utils.get_local_path(url, 'cleaned')
            if os.path.exists(dest):
                if self.verbose:
                    print 'Skip clean of %s as clean version already exists' % src
                continue
            if self.verbose:
                print 'Formatting %s to %s' % (src, dest)
            infile = file(src)
            if src.endswith('wssnt10.txt'): # if it is the sonnets need a hack
                # delete last 140 characters
                tmp1 = infile.read()
                infile = StringIO.StringIO(tmp1[:-120])
            formatter = GutenbergShakespeare(infile)
            ff = file(dest, 'w')
            out = formatter.extract_text()
            ff.write(out)
            ff.close()

    def title_to_name(self, title):
        """Convert a title to a unique name
        """
        tmp1 = title.replace(',', '')
        tmp1 = tmp1.replace("'", '')
        tmp1 = tmp1.lower()
        stripwords = [ 'king ', 'a ', 'the ' ]
        for ww in stripwords:
            if tmp1.startswith(ww):
                tmp1 = tmp1[len(ww):]
        tmp1 = tmp1.strip()
        tmp1 = tmp1.replace(' ', '_')
        return tmp1

    
    def add_to_db(self):
        """Add all gutenberg texts to the db list of texts.
        
        If a text already exists in the db it will be skipped.
        """
        import shakespeare.dm
        for text in self._index:
            title = text[0]
            name = self.title_to_name(title) + '_gut'
            cachePath = shakespeare.utils.get_local_path(text[1], 'cleaned')
            notes = 'Sourced from Project Gutenberg (url=%s). %s' % (text[1],
                    text[2])
            if text[2] == 'folio':
                name += '_f'
            
            numExistingTexts = shakespeare.dm.Material.select(
                        shakespeare.dm.Material.q.name==name).count()
            if numExistingTexts > 0:
                if self.verbose:
                    print('Skip: Add to db. Gutenberg text already exists with name: %s' % name)
            else:
                if self.verbose:
                    print('Add to db. Gutenberg text named [%s]' % name)
                shakespeare.dm.Material(name=name,
                                        title=title,
                                        creator='Shakespeare, William',
                                        cache_path=cachePath,
                                        notes=notes)

