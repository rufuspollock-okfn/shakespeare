'''Support for indexing and searching texts using xapian.

Architecture
============

For information on theoretical structure of Xapain see:
http://xapian.org/docs/intro_ir.html

For basic demo python code see: http://xapian.org/docs/bindings/python/

For helpful example of using Xapian in python (including metadata, add_post
etc) see:

  * http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/
  * http://www.rkblog.rk.edu.pl/w/p/xapian-python/

Here we discuss how we can use Xapian in OS. Two main tasks:

    1. Do search
    2. Produce statistics

Second task just requires stemming support, first requires full Xapian
facilities. Main question for indexing is:

  * What is our atomization level. I.e. what are 'documents' we index? Is it:
    * A whole poem or play
    * Is it a paragraph within a work
    * Is it a character's whole speech?

TODO:
    * add metadata (e.g. which character is speaking, work id ...)
'''
import os
import re

import xapian

class SearchIndex(object):
    def __init__(self, index_dir):
        self.index_dir = index_dir

    @classmethod
    def config_index_dir(self):
        '''Get the search index directory specified in the config.'''
        import shakespeare
        conf = shakespeare.conf()
        index_dir = conf['search_index_dir']
        return index_dir

    @classmethod
    def default_index(self):
        '''Return a SearchIndex instance initialized with the path specified in
        the configuration file.
        '''
        index_dir = self.config_index_dir()
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)
        return SearchIndex(index_dir)

    @classmethod
    def get_stats(self, fileobj):
        '''Get statistics on text in fileobj.

        Words are stemmed so that e.g. love and loved count as the same word.
        '''
        # (?) maybe could use xapian.TermGenerator to split document
        WORD_RE = re.compile('\\w{1,32}', re.U)
        stemmer = xapian.Stem('english')
        results = {}
        text = fileobj.read()
        text = text.encode('utf8')
        for term in WORD_RE.finditer(text):
            word = term.group()
            word = word.lower()
            stemmed_word = stemmer(word)
            results[stemmed_word] = results.get(stemmed_word, 0) + 1
        return results

    def add_item(self, fileobj):
        document = xapian.WritableDatabase (self.index_dir, xapian.DB_CREATE_OR_OPEN)
        indexer = xapian.TermGenerator()
        stemmer = xapian.Stem("english")
        indexer.set_stemmer(stemmer)

        para = ''
        try:
            for line in fileobj:
                line = line.strip()
                if line == '':
                    if para != '':
                        doc = xapian.Document()
                        doc.set_data(para)

                        indexer.set_document(doc)
                        # this *will* include positional information
                        indexer.index_text(para)

                        # Add the document to the database.
                        document.add_document(doc)
                        para = ''
                else:
                    if para != '':
                        para += '\n'
                    para += line
        except StopIteration:
            # TODO: what is happening here?
            pass

    def search(self, query_string):
        # Open the database for searching.
        database = xapian.Database(self.index_dir)

            # Start an enquire session.
        enquire = xapian.Enquire(database)

        # Parse the query string to produce a Xapian::Query object.
        qp = xapian.QueryParser()
        stemmer = xapian.Stem("english")
        qp.set_stemmer(stemmer)
        qp.set_database(database)
        qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        query = qp.parse_query(query_string)
        print "Parsed query is: %s" % query.get_description()

         # Find the top 10 results for the query.
        enquire.set_query(query)
        # get search results offset, offset+count
        offset = 0
        count = 10
        matches = enquire.get_mset(offset, count)
        return matches

    @classmethod
    def print_matches(self, matches):
        # Display the results.
        print "%i results found." % matches.get_matches_estimated()
        print "Results 1-%i:" % matches.size()

        for m in matches:
            print "%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())

