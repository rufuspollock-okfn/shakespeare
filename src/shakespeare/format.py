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
    elif format == 'annotate':
        formatter = TextFormatterAnnotate(fileobj)
    else:
        raise ValueError('Unknown format: %s' % format)
    return formatter.format()


class TextFormatter(object):
    """Abstract base class for formatters.
    """

    def __init__(self, file=None):
        """
        @file: file-like object containing a text in plain txt with utf-8
        encoding
        """
        self.file = file

    def format(self):
        """Format the supplied text.

        The returned string will be in unicode format with utf-8 encoding
        """
        raise NotImplementedError()

    def escape_chars(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;')

class TextFormatterPlain(TextFormatter):
    """Format the text as plain text (in an html <pre> tag).
    """

    def format(self):
        out = unicode(self.file.read(), 'utf-8')
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

    def format(self):
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = unicode(count).ljust(4) # assume line no < 10000
            tline = unicode(line, 'utf-8').rstrip() 
            tline = self.escape_chars(tline)
            result += u'<pre id="%s">%s %s</pre>\n' % (count, tlineno, tline)
            count += 1
        return result


class TextFormatterAnnotate(TextFormatter):
    """Format the text in a manner suitable for marginalia annotation.
    """
    entry_template = u'''
    <div id="%(id)s" class="hentry">
        <h3 class="entry-title">%(title)s</h3>
        <div class="entry-content">
            %(content)s
        </div><!-- /entry-content -->
        <p class="metadata">
            <a rel="bookmark" href="%(page_url)s#%(id)s">#</a>
            <span class="author">%(author)s</span>
        </p>
        <div class="notes">
            <button class="createAnnotation" onclick="createAnnotation('%(id)s',true)" title="Click here to create an annotation">&gt;</button>
            <ol>
                <li></li>
            </ol>
        </div><!-- /notes -->
    </div><!-- /hentry -->
'''

    def format(self):
        line_numberer = TextFormatterLineno(self.file)
        text_with_linenos = line_numberer.format()
        # todo chunking
        values = {
                'content' : text_with_linenos,
                'title' : 'Test Stuff',
                'id' : 'm2',
                'page_url' : 'http://localhost:8080/',
                'author' : 'Nemo',
                }
        result = self.entry_template % values
        return result

