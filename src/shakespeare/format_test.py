import StringIO
import shakespeare.format

sometext = '''Blah
blah blah'''

class TestTextFormatterPlain:
    fileobj = StringIO.StringIO(sometext)
    formatter = shakespeare.format.TextFormatterPlain(fileobj)
    exp = '''
<pre>
    %s
</pre>''' % sometext

    def test_format(self):
        out = self.formatter.format()
        assert out == self.exp

class TestTextFormatterLineno:
    fileobj = StringIO.StringIO(sometext)
    formatter = shakespeare.format.TextFormatterLineno(fileobj)
    exp = '''<pre id="0">0    Blah</pre>
<pre id="1">1    blah blah</pre>
'''

    def test_format(self):
        out = self.formatter.format()
        assert out == self.exp

def test_text_format():
    formatlist = [ ('plain', TestTextFormatterPlain),
        ('lineno', TestTextFormatterLineno)
        ]
    for item in formatlist:
        fileobj = StringIO.StringIO(sometext)
        tout = shakespeare.format.format_text(fileobj, item[0])
        assert tout == item[1].exp
