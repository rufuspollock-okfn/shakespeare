import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import shakespeare.lib.helpers as h

from shakespeare.lib.base import BaseController, render
import shakespeare.lib.feed as feed
import shakespeare.model.word as word

log = logging.getLogger(__name__)

class CronController(BaseController):

    def index(self):
        out = '''<pre>
Cron Jobs - for sysadmin use

work_introductions: %s
word_of_the_day: %s
</pre>
    '''
        out = out % (
            feed.WorkIntroductionLoader.__doc__,
            word.load_word_info_from_feed.__doc__
            )
        return out

    def work_introductions(self):
        loader = feed.WorkIntroductionLoader()
        results = loader.load_feed()
        stringified = [ '%s: %s' % (r[0], unicode(r[1])[:80]) for r in results ]
        out = u'<pre>%s</pre>' % h.escape('\n'.join(stringified))
        return out

    def word_of_the_day(self):
        import shakespeare.model.word as word
        word.load_word_info_from_feed()
        return 'Processed all entries ok'
        
