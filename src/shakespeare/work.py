import os

import utils
import conf


class GutenbergIndex(object):
    """Parse the index of Gutenberg works so as to find Shakespeare works.
    """
    
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
        ff = file(utils.get_cache_path('GUTINDEX.ALL'))
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


class ShakespeareIndex(object):

    def __init__(self):
        gutindex = GutenbergIndex()
        self.all = gutindex.get_shakespeare_list()
        # todo: parse it up
        self.folios = None
        self.nonfolios = None
        self.sonnets = None

index = ShakespeareIndex()

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
