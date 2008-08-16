import logging

from shakespeare.lib.base import *

log = logging.getLogger(__name__)

import shakespeare.search

class SearchController(BaseController):

    def index(self):
        c.query = request.params.get('query', '')
        if c.query:
            c.matches = self._get_matches(c.query)
            c.results = self._get_results(c.matches)
            c.total = c.matches.get_matches_estimated()
        else:
            c.matches = None
        return render('search/index')
    
    def _get_matches(self, query):
        index = shakespeare.search.SearchIndex.default_index()
        matches = index.search(query, numresults=50)
        return matches

    def _get_results(self, matches):
        results = []
        for m in matches:
            text, lineno = self._match_to_text(m)
            if text:
                # slight hack -- just attach direct to object
                text._lineno = lineno
                text._snippet = m.document.get_data()
                results.append(text)
            else:
                # TODO: create a dummy text ...
                pass
        return results

    def _match_to_text(self, m):
        item_id = m.document.get_value(shakespeare.search.ITEM_ID)
        text = model.Material.byName(item_id)
        lineno = m.document.get_value(shakespeare.search.LINE_NO)
        return (text, lineno)

