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

    def __init__(self, file):
        """
        @file: file-like object containing a text in plain txt
        """
        self.file = file

    def format(self):
        """Format the supplied text.
        """
        raise NotImplementedError()

class TextFormatterPlain(TextFormatter):
    """Format the text as plain text (in an html <pre> tag).
    """

    def format(self):
        out = \
'''
<pre>
    %s
</pre>''' % self.file.read()
        return out

class TextFormatterLineno(TextFormatter):
    """Format the text to have line numbers.
    """

    def format(self):
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = str(count).ljust(4) # assume line no < 10000
            result += '<pre id="%s">%s %s</pre>\n' % (count, tlineno, line.rstrip())
            count += 1
        return result
