import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

import shakespeare.search

class SearchController(BaseController):

    def index(self):
        c.query = request.params.get('query', '')
        if c.query:
            matches = self._get_matches(c.query)
            c.results = [ SearchResult.from_match(m) for m in matches ]
            c.total = matches.get_matches_estimated()
        else:
            c.total = -1
        return render('search/index')
    
    def _get_matches(self, query):
        index = shakespeare.search.SearchIndex.default_index()
        matches = index.search(query, numresults=50)
        return matches

class SearchResult(object):
    def __init__(self, snippet='', text=None, lineno=None):
        for k,v in locals().items():
            setattr(self, k, v)
        if self.text:
            self.title = self.text.title
        else:
            self.title = 'Unknown'

    @classmethod
    def from_match(cls, m):
        snippet = m.document.get_data()
        item_id = m.document.get_value(shakespeare.search.ITEM_ID)
        text = model.Material.byName(item_id)
        lineno = m.document.get_value(shakespeare.search.LINE_NO)
        return cls(snippet, text, lineno)

