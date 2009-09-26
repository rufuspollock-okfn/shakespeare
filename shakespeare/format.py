"""
Format texts in a variety of ways
"""

def format_text(fileobj, format):
    """Format a provided text in a variety of ways.

    @format: the name specifying the format to use
    """
    formatter = None
    if format == 'plain':
        formatter = TextFormatterPlain()
    elif format == 'lineno':
        formatter = TextFormatterLineno()
    elif format == 'annotate':
        formatter = TextFormatterAnnotate()
    else:
        raise ValueError('Unknown format: %s' % format)
    return formatter.format(fileobj)


class TextFormatter(object):
    """Abstract base class for formatters.
    """

    def format(self, file):
        """Format the supplied text.

        @file: file-like object containing a text in plain txt with utf-8
        encoding

        @return a string in unicode format with utf-8 encoding
        """
        raise NotImplementedError()

    def escape_chars(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;')
    

class TextFormatterPlain(TextFormatter):
    """Format the text as plain text (in an html <pre> tag).
    """

    def format(self, file):
        self.file = file
        out = self.file.read()
        if not isinstance(out, unicode):
            out = unicode(out, 'utf-8')
        out = self.escape_chars(out)
        out = \
u'''
<pre>
    %s
</pre>''' % out
        return out


class TextFormatterLineno(TextFormatter):
    """Format the text to have line numbers.
    """

    def format(self, file):
        self.file = file
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = unicode(count).ljust(4) # assume line no < 10000
            tline = line
            if not isinstance(tline, unicode):
                tline = unicode(tline, 'utf-8')
            tline = tline.rstrip() 
            tline = self.escape_chars(tline)
            result += u'<pre id="%s">%s %s</pre>\n' % (count, tlineno, tline)
            count += 1
        return result


