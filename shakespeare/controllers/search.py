import logging

from shakespeare.lib.base import *
from shakespeare.lib.helpers import Page
import shakespeare.search

log = logging.getLogger(__name__)


class SearchController(BaseController):

    def index(self):
        c.query = request.params.get('query', '')
        items_per_page = 50
        page = int(request.params.get('page', 1))
        if c.query:
            index = shakespeare.search.SearchIndex.default_index()
            matches = index.search(c.query, offset=items_per_page*(page-1),
                    numresults=items_per_page)
            c.results = [ SearchResult.from_match(m) for m in matches ]
            c.total = matches.get_matches_estimated()
            # unfortunately Page does not deal well with only being given
            # "current" (i.e .this page's) set of results (e.g. if you ask for
            # page 2 and just give the 50 results for page 2 nothing will be
            # displayed as it tries to offset 50 into a result set with only 50
            # results ...)
            c.page = Page(
                collection=c.results,
                page=page,
                items_per_page=items_per_page,
                item_count=c.total
            )
        return render('search/index.html')
    

class SearchResult(object):
    def __init__(self, snippet, text, lineno=None):
        self.snippet = snippet
        self.text = text
        self.lineno = lineno

    @classmethod
    def from_match(cls, m):
        snippet = m.document.get_data()
        item_id = m.document.get_value(shakespeare.search.ITEM_ID)
        text = model.Material.by_name(item_id)
        lineno = m.document.get_value(shakespeare.search.LINE_NO)
        return cls(snippet, text, lineno)

