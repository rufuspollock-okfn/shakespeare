"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
try:
    from webhelpers.rails.wrapped import *
except:
    pass
from routes import url_for
