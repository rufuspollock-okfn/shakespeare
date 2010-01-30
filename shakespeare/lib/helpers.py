"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
# wrap markdown in literal so not escaped by genshi
from webhelpers.markdown import markdown as _markdown
def _new_markdown(*args, **kwargs):
    return literal(_markdown(*args, **kwargs))
markdown = _new_markdown

from routes import url_for, redirect_to

