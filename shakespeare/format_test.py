import StringIO
import shakespeare.format


starttext = unicode('''Blah \xc3\xa6
blah & blah''', 'utf-8')

sometext = starttext.replace('&', '&amp;')

class TestTextFormatter:
    formatter = shakespeare.format.TextFormatter()

    def test_escape_chars(self):
        out = self.formatter.escape_chars(starttext)
        assert out == sometext


class TestTextFormatterPlain:
    fileobj = StringIO.StringIO(starttext.encode('utf-8'))
    formatter = shakespeare.format.TextFormatterPlain()
    exp = u'''
<pre>
    %s
</pre>''' % sometext

    def test_format(self):
        out = self.formatter.format(self.fileobj)
        assert out == self.exp


class TestTextFormatterLineno:
    fileobj = StringIO.StringIO(starttext.encode('utf-8'))
    formatter = shakespeare.format.TextFormatterLineno()
    exp = u'''<pre id="0">0    Blah \xe6</pre>
<pre id="1">1    blah &amp; blah</pre>
'''

    def test_format(self):
        out = self.formatter.format(self.fileobj)
        assert out == self.exp


class TestTextFormatterAnnotate:

    fileobj = StringIO.StringIO(starttext.encode('utf-8'))
    formatter = shakespeare.format.TextFormatterAnnotate()
    
    def test_format(self):
        self.fileobj.seek(0)
        page_url = 'http://somethingelse.com/'
        newtitle = 'New Title'
        out = self.formatter.format(
                self.fileobj,
                page_uri=page_url,
                title=newtitle,
                )
        print '"%s"' % out.encode('utf-8')
        assert page_url in out
        assert newtitle in out
        assert TestTextFormatterLineno.exp in out
        # test valid xml
        import genshi
        outxml = genshi.XML(out)


def test_text_format():
    formatlist = [ ('plain', TestTextFormatterPlain),
        ('lineno', TestTextFormatterLineno),
        ]
    for item in formatlist:
        fileobj = StringIO.StringIO(starttext.encode('utf-8'))
        tout = shakespeare.format.format_text(fileobj, item[0])
        assert tout == item[1].exp

