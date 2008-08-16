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

# keys for document values
ITEM_ID = 0
LINE_NO = 1

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

    def add_item(self, fileobj, item_id=None):
        database = xapian.WritableDatabase(self.index_dir, xapian.DB_CREATE_OR_OPEN)
        indexer = xapian.TermGenerator()
        stemmer = xapian.Stem("english")
        indexer.set_stemmer(stemmer)

        para = ''
        try:
            count = -1
            para_start = 0
            for line in fileobj:
                count += 1
                line = line.strip()
                if line == '':
                    if para != '':
                        doc = xapian.Document()
                        doc.set_data(para)
                        id_term = 'I' + str(item_id)
                        doc.add_term(id_term)
                        doc.add_value(ITEM_ID, str(item_id))
                        doc.add_value(LINE_NO, str(para_start))

                        indexer.set_document(doc)
                        # this *will* include positional information
                        indexer.index_text(para)

                        database.add_document(doc)
                        # assume next para starts
                        para = ''
                    # must come after
                    para_start = count
                else:
                    if para != '':
                        para += '\n'
                    para += line
        except StopIteration:
            # TODO: what is happening here?
            raise

    def get_database(self):
        database = xapian.Database(self.index_dir)
        return database

    def search(self, query_string, offset=0, numresults=10):
        database = self.get_database()
        enquire = xapian.Enquire(database)
        qp = xapian.QueryParser()
        stemmer = xapian.Stem("english")
        qp.set_stemmer(stemmer)
        qp.set_database(database)
        qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        query = qp.parse_query(query_string)
        enquire.set_query(query)
        matches = enquire.get_mset(offset, numresults)
        return matches

    def add_from_path(self, path):
        '''Add contents of {path} (file itself or all text files in directory
        if directory) to the search index.'''
        path = path.strip()
        if not os.path.exists(path):
            print '"%s" is not an existent path' % path
            return 1
        if os.path.isdir(path):
            fns = os.listdir(path)
            fns = filter(lambda x: x.endswith('.txt'), fns)
            works = [ os.path.join(path, fn) for fn in fns ]
        else:
            works = [ path ]
        for work in works:
            fileobj = open(work)
            self.add_item(fileobj)

    @classmethod
    def print_matches(self, matches):
        # Display the results.
        msg = '%i results found.' % matches.get_matches_estimated()
        msg += 'Results 1-%i:' % matches.size()

        for m in matches:
            msg += '\n'
            msg += '%i: %i%% docid=%i' % (m.rank + 1, m.percent, m.docid)
            msg += '\n'
            msg += m.document.get_data()
            msg += '\n'
        return msg
    
