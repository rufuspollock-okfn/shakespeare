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

class TextFormatter(object):
    """Format a provided text in a variety of ways.
    For example: add line numbers, convert to html with line ids etc
    """

    def __init__(self, file):
        """
        @file: file-like object containing a text in plain txt
        """
        self.file = file

    def format(self, format):
        """
        @format: the name specifying the format to use
        """
        if format == 'lineno':
            return self.add_line_numbers()
        else:
            raise ValueError('Unknown format: %s' % format)
    
    def add_line_numbers(self):
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = str(count).ljust(4) # assume line no < 10000
            result += '<pre id="%s">%s %s</pre>\n' % (count, tlineno, line.rstrip())
            count += 1
        return result
