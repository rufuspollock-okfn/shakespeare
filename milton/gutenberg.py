"""Various useful functionality related to Project Gutenberg
"""
import os
import StringIO
import milton.cache


class GutenbergIndex(object):
    """Parse the index of Gutenberg works so as to find Milton works.

   
    """
    
    # url for the Gutenberg index file
    gutindex = 'http://www.gutenberg.org/dirs/GUTINDEX.ALL'

    def __init__(self):
        self.download_gutenberg_index()
        self._gutindex_local_path = milton.cache.default.path(self.gutindex)

    def download_gutenberg_index(self):
        """Download the Gutenberg Index file GUTINDEX.ALL to cache if we don't
        have it already.
        """
        milton.cache.default.download_url(self.gutindex)

    def make_url(self, year, idStr):
        return 'http://www.gutenberg.org/dirs/etext%s/%s10.txt' % (year[2:], idStr)

    def get_milton_list(self):
        """Get list of milton works and urls.

        Results are sorted by work title.

        """
        # results have format [ title, url, comments ]
        results = [ ["Areopagitica", 'http://www.gutenberg.org/files/608/608.txt', ''] ]
        results.append(["L'Allegro, Il Penseroso, Comus, and Lycidas",
                'http://www.gutenberg.org/dirs/etext96/miltp10.txt', '']
                )
        results.append(["Comus",
                'http://www.gutenberg.org/files/19819/19819.txt', '']
                )
        results.append(["Paradise Lost (No introduction)",
                'http://www.gutenberg.org/dirs/etext91/plboss10.txt', '']
                )
        
        results.append(["Paradise Regained",
                'http://www.gutenberg.org/dirs/etext93/rgain10.txt', '']
                )

        results.append(["Poemata",
                'http://www.gutenberg.org/dirs/etext04/poema10.txt', '']
                )
        
        results.append(["Poetical Works",
                'http://www.gutenberg.org/dirs/etext99/pmsjm10.txt', '']
                )
        def compare_list(item1, item2):
            if item1[0] > item2[0]: return 1
            else: return -1
        results.sort(compare_list)
        return results

"""
Clean up Gutenberg texts by removing all the header and footer bumpf
"""

import re

headerEndPhrases = ['START OF THIS PROJECT', 'START OF THE PROJECT', 'THE SMALL PRINT! FOR PUBLIC DOMAIN']
notesStartPhrases = ["Executive Director's Notes:"]
notesEndPhrases = ['Produced by']
footerStartPhrases = ['End of Project Gutenberg', 'End of The Project Gutenberg', 'END OF THE PROJECT GUTENBERG EBOOK']

def make_re_from_phrase(phrase):
    """
    Make a regular expression that matches a phrase and its surrounding
    paragraph, i.e. that look like:
    
    ... phrase ....
    more text
    [blank]
    [blank]+
    """
    # need \S to ensure not just whitespace
    paragraphText = '(.+\S.+\n)*' 
    # [[TODO: check slowdown due to inclusion of '^.*' at start
    tmp = '^.*' + phrase + '.*\n' + paragraphText + '\s+'
    return re.compile(tmp, re.I | re.M)  # make it case insensitive

class Gutenbergmilton(object):
    """
    Process Gutenberg Milton texts
    """
    
    def __init__(self, etext):
        """
        @param etext: file like object containing the etext
        
        Procedure:
            1. strip out header and footer bumpf
            2. are there notes? If so strip them out
        """
        self.etext = etext
        # most milton texts are either ascii or latin-1
        self.etextStr = unicode(self.etext.read(), 'latin-1').encode('utf-8')
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
        self.footerStart = self.get_footer_start()
        self.headerEnd = self.get_header_end()
        startIndex = self.headerEnd
        if self.notesEnd > 0:
            startIndex = self.notesEnd
        return self.etextStr[startIndex : self.footerStart].rstrip()
        
    def get_notes_end(self):
        "Return 0 if no notes"
        indices = [ self._find_min(phrase, self.etextStr) for phrase in notesEndPhrases]
        index = min(indices)
        return index
    
    def get_header_end(self):
        indices = [ self._find_max(phrase, self.etextStr) for phrase in headerEndPhrases]
        return max(indices)
    
    def get_footer_start(self):
        indices = [ self._find_min(phrase, self.etextStr) for phrase in footerStartPhrases]
        return min(indices)



class Helper(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        gutindex = GutenbergIndex()
        self._index = gutindex.get_milton_list()
     
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

    def execute(self, line=None):
        self.download(line)
        self.clean(line)
        self.add_to_db()

    def get_index(self, line=None):
        """Get list of texts
        """
        return self._index

    def download(self, line=None):
        """Download from Project Gutenberg all the milton texts listed in the
        index.
        """
        for item in self._index:
            title = item[0]
            url = item[1]
            if self.verbose:
                print 'Downloading %s (%s)' % (url, title)
            milton.cache.default.download_url(item[1])
    
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
            src = milton.cache.default.path(url)
            dest = milton.cache.default.path(url, 'plain')
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
            formatter = Gutenbergmilton(infile)
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
        import milton.model
        for text in self._index:
            title = text[0]
            name = self.title_to_name(title) + '_gut'
            url = text[1]
            notes = 'Sourced from Project Gutenberg (url=%s). %s' % (text[1],
                    text[2])
            if text[2] == 'folio':
                name += '_f'
            
            numExistingTexts = milton.model.Material.select(
                        milton.model.Material.q.name==name).count()
            if numExistingTexts > 0:
                if self.verbose:
                    print('Skip: Add to db. Gutenberg text already exists with name: %s' % name)
            else:
                if self.verbose:
                    print('Add to db. Gutenberg text named [%s]' % name)
                milton.model.Material(name=name,
                                        title=title,
                                        creator='Milton, John',
                                        url=url,
                                        notes=notes)

