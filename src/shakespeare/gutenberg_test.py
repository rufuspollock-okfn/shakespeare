import shakespeare.gutenberg
import shakespeare.utils as utils
from shakespeare.gutenberg import make_re_from_phrase, GutenbergShakespeare 

class TestGutenbergIndex:

    gutindex = shakespeare.gutenberg.GutenbergIndex()
    
    def test_parse_line_for_folio(self):
        inStr = 'Jul 2000 Cymbeline, by Wm. Shakespeare  [First Folio]=[FF] [0ws39xxx.xxx] 2269'
        out = self.gutindex.parse_line_for_folio(inStr)
        exp = ['Cymbeline', '2000', '0ws39']
        for ii in range(len(exp)):
            assert out[ii] == exp[ii]
    
    def test_parse_line_for_normal(self):
        inStr = 'Nov 1998 Cymbeline, by William Shakespeare [2ws39xxx.xxx] 1538'
        out = self.gutindex.parse_line_for_normal(inStr)
        exp = ['Cymbeline', '1998', '2ws39']
        for ii in range(len(exp)):
            assert out[ii] == exp[ii]
    
    def test_make_url(self):
        exp = 'http://www.gutenberg.org/dirs/etext00/0ws3910.txt'
        out = self.gutindex.make_url('2000', '0ws39')
        assert exp == out
    
    def test_make_url_2(self):
        exp = 'http://www.gutenberg.org/dirs/etext98/2ws3910.txt'
        out = self.gutindex.make_url('1998', '2ws39')
        assert exp == out
    
    def test__extract_shakespeare_works(self):
        plays = self.gutindex._extract_shakespeare_works()
        assert len(plays) == 73


class TestFormat:
    
    def test_make_re_from_phrase(self):
        outStr = """blah
            
            
            """
        inStr = outStr + 'All is Well that'
        regex = make_re_from_phrase('blah')
        out = regex.search(inStr)
        assert out.group() == outStr
    
    def test_makeReFromPhrase2(self):
        outStr = """blah
            joe
            hello
            
            
            """
        inStr = outStr + 'All is Well that'
        regex = make_re_from_phrase('blah')
        out = regex.search(inStr)
        assert out.group() == outStr

class TestGutenbergShakespeare:
    # As you like it in Folio and normal
    url1 = 'http://www.gutenberg.org/dirs/etext00/0ws2510.txt'
    url2 = 'http://www.gutenberg.org/dirs/etext98/2ws2510.txt'
    utils.download_url(url1)
    utils.download_url(url2)
    etext1 = file(utils.get_local_path(url1))
    etext2 = file(utils.get_local_path(url2))
    gut1 = GutenbergShakespeare(etext1)
    gut2 = GutenbergShakespeare(etext2)
    
    def test_get_header_end(self):
        out = self.gut1.get_header_end()
        exp = self.gut1.etextStr.index("Executive Director's Notes:")
        assert out == exp
    
    def test_get_footer_start(self):
        out = self.gut1.get_footer_start()
        # has no footer 
        exp = len(self.gut1.etextStr)
        assert out == exp
        
        out = self.gut2.get_footer_start()
        exp = self.gut2.etextStr.index("End of Project Gutenberg Etext of As You Like It by Shakespeare")
        assert out == exp
    
    def test_get_notes_end(self):
        out = self.gut1.get_notes_end()
        exp = self.gut1.etextStr.index("As you Like it\n\nActus")
        assert out == exp

    def test_extract_text(self):
        # [[TODO: run this test on all of the etexts]]
        for gut in [self.gut1, self.gut2]:
            out = gut.extract_text()
            notFound = (out.find('Gutenberg') == -1)
            assert notFound

#    def test_get_etext_url(self):
#        number = 11125
#        exp = 'http://www.gutenberg.org/dirs/1/1/1/2/11125/11125.txt'
#        out = get_etext_url(number)
#        self.assertEqual(out, exp)

import shakespeare.dm
class TestHelper:
    url1 = 'http://www.gutenberg.org/dirs/etext00/0ws2510.txt'
    url2 = 'http://www.gutenberg.org/dirs/etext98/2ws2510.txt'
    helper = shakespeare.gutenberg.Helper()

    def test_clean(self):
        line = '%s %s' % (self.url1, self.url2)
        self.helper.clean(line)

    def test_get_index(self):
        out = self.helper.get_index()
        assert 74 == len(out)

    def test_title_to_name(self):
        inlist = [ 'King Henry VIII', 
                   'The Merchant of Venice',
                   'Twelfth Night',
                   "All's Well That Ends Well",
                   ]
        explist = [ 'henry_viii',
                    'merchant_of_venice',
                    'twelfth_night',
                    'alls_well_that_ends_well',
                    ]
        for ii in range(len(inlist)):
            assert explist[ii] == self.helper.title_to_name(inlist[ii])

    def test_add_to_db(self):
        self.helper.add_to_db()
        text1 = shakespeare.dm.Material.byName('hamlet_gut')
        shakespeare.dm.Material.byName('hamlet_gut_f')
        assert 'Shakespeare, William' == text1.creator
        alltexts = shakespeare.dm.Material.select()
        # do not delete because we may remove stuff that was there
        # though this may undermine tests
        # TODO: sort this out satisfactorily 
        # for text in alltexts:
        #    if '_gut' in text.name:
        #        shakespeare.dm.Material.delete(text.id)

