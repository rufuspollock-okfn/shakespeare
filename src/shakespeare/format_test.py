import StringIO
import shakespeare.format


starttext = '''Blah
blah & blah'''

sometext = starttext.replace('&', '&amp;')

class TestTextFormatter:
    formatter = shakespeare.format.TextFormatter()

    def test_escape_chars(self):
        out = self.formatter.escape_chars(starttext)
        assert out == sometext


class TestTextFormatterPlain:
    fileobj = StringIO.StringIO(starttext)
    formatter = shakespeare.format.TextFormatterPlain(fileobj)
    exp = '''
<pre>
    %s
</pre>''' % sometext

    def test_format(self):
        out = self.formatter.format()
        assert out == self.exp


class TestTextFormatterLineno:
    fileobj = StringIO.StringIO(starttext)
    formatter = shakespeare.format.TextFormatterLineno(fileobj)
    exp = '''<pre id="0">0    Blah</pre>
<pre id="1">1    blah &amp; blah</pre>
'''

    def test_format(self):
        out = self.formatter.format()
        assert out == self.exp

def test_text_format():
    formatlist = [ ('plain', TestTextFormatterPlain),
        ('lineno', TestTextFormatterLineno)
        ]
    for item in formatlist:
        fileobj = StringIO.StringIO(starttext)
        tout = shakespeare.format.format_text(fileobj, item[0])
        assert tout == item[1].exp
