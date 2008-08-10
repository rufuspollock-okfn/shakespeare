# Support for indexing and searching texts using xapian
import os

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

    def add_item(self, fileobj):
        # TODO: remove this comment as no longer relevant (?)
        #create the folder for a writable db: alter path
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
                        indexer.index_text(para)

                        # Add the document to the database.
                        document.add_document(doc)
                        para = ''
                else:
                    if para != '':
                        para += ' '
                    para += line
        except StopIteration:
            # TODO: what is happening here?
            pass
            print Stopped

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
        matches = enquire.get_mset(0, 10)
        return matches

    @classmethod
    def print_matches(self, matches):
        # Display the results.
        print "%i results found." % matches.get_matches_estimated()
        print "Results 1-%i:" % matches.size()

        for m in matches:
            print "%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())

