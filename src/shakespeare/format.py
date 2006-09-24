"""
Format texts in a variety of ways
"""

def format_text(fileobj, format):
    """Format a provided text in a variety of ways.

    @format: the name specifying the format to use
    """
    formatter = None
    if format == 'plain':
        formatter = TextFormatterPlain(fileobj)
    elif format == 'lineno':
        formatter = TextFormatterLineno(fileobj)
    else:
        raise ValueError('Unknown format: %s' % format)
    return formatter.format()


class TextFormatter(object):
    """Abstract base class for formatters.
    """

    def __init__(self, file=None):
        """
        @file: file-like object containing a text in plain txt
        """
        self.file = file

    def format(self):
        """Format the supplied text.
        """
        raise NotImplementedError()

    def escape_chars(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;')

class TextFormatterPlain(TextFormatter):
    """Format the text as plain text (in an html <pre> tag).
    """

    def format(self):
        out = self.file.read()
        out = self.escape_chars(out)
        out = \
'''
<pre>
    %s
</pre>''' % out
        return out

class TextFormatterLineno(TextFormatter):
    """Format the text to have line numbers.
    """

    def format(self):
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = str(count).ljust(4) # assume line no < 10000
            tline = line.rstrip() 
            tline = self.escape_chars(tline)
            result += '<pre id="%s">%s %s</pre>\n' % (count, tlineno, tline)
            count += 1
        return result
