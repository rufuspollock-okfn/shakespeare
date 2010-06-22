import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from shakespeare.lib.base import BaseController, render
import shakespeare.model as model

log = logging.getLogger(__name__)

class WordController(BaseController):

    def index(self):
        c.words = model.Word.all()
        return render('word/index.html')

    def read(self, id):
        name = id.lower()
        c.word = model.Word.by_name(name)
        return render('word/read.html')

