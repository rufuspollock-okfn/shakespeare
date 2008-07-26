import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

import shakespeare.search

class SearchController(BaseController):

    def index(self):
        query = request.params.get('query', '')
        if query:
            c.matches = self._get_results(query)
            c.total = c.matches.get_matches_estimated()
        else:
            c.matches = None
        return render('search/index')
    
    def _get_results(self, query):
        index = shakespeare.search.SearchIndex.default_index()
        matches = index.search(query)
        return matches
        

