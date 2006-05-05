import os
import urllib

from utils import *
import conf

def download_gutenberg_index():
    "Download the Gutenberg Index file GUTINDEX.ALL."
    download_url(conf.GUTINDEX)

def download_all_shakespeare():
    """Download from Project Gutenberg all the shakespeare texts listed in
    the index.
    """
    index = make_index()
    for item in index:
        download_url(item[1])

def make_url(year, idStr):
    return 'http://www.gutenberg.org/dirs/etext%s/%s10.txt' % (year[2:], idStr)

def make_index():
    """Get full list of shakespeare works and urls.
    Results are sorted by work title.
    """
    # results have format [ title, url, comments ]
    # folio in comments indicates it is a first folio
    results = [ ["Sonnets", 'http://www.gutenberg.org/dirs/etext97/wssnt10.txt', ''] ]
    plays = get_list_of_plays()
    for play in plays:
        url = make_url(play[1], play[2])
        results.append([play[0], url, play[3]])
    def compare_list(item1, item2):
        if item1[0] > item2[0]: return 1
        else: return -1
    results.sort(compare_list)
    return results

def get_list_of_plays():
    """Get list of Gutenberg plays consisting of folio and one other
    'standard' version.
    @return: list consisting of tuples in form [title, year, id, comment]
    """
    ff = file(get_cache_path('GUTINDEX.ALL'))
    results = []
    for line in ff.readlines():
        result = parse_line_for_folio(line)
        if result:
            results.append(result + ['folio'])
        resultNormal = parse_line_for_normal(line)
        if resultNormal:
            results.append(resultNormal + [''])
    return results

def parse_line_for_normal(line):
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
    
def parse_line_for_folio(line):
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
