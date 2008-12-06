import logging

import genshi

from shakespeare.lib.base import *

import shakespeare
import shakespeare.format
import shakespeare.model as model

# import this after dm so that db connection is set
# import annotater.store
# import annotater.marginalia

log = logging.getLogger(__name__)


class SiteController(BaseController):

    def index(self):
        return render('index.html')

    def about(self):
        return render('about.html')

    def guide(self):
        return render('guide.html')

