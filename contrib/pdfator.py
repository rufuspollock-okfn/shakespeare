import os
import re

import shakespeare.cache
import shakespeare.gutenberg

class Pdfator(object):
    '''
    # 0. retrieve
    # 1. get rid of gutenberg stuff
    # 2. markup where possible (for latex)
    # 3. latexize
    # 4. pdfize
    '''

    def __init__(self, cachedir):
        self.cachedir = cachedir
        self.cache = shakespeare.cache.Cache(cachedir)

    def execute(self, text_url):
        self.cache.download_url(text_url)
        localpath = self.cache.path(text_url)
        cleaner = shakespeare.gutenberg.GutenbergCleaner(open(localpath))
        text = cleaner.extract_text()
        latex_template = r'''
\documentclass[a5paper]{memoir}
\usepackage{verse}
\usepackage{dramatist}

\title{Testing}

\begin{document}
\frontmatter
\pagestyle{empty}
\maketitle
\clearpage

\tableofcontents

\mainmatter
%s

\end{document}
'''
        final = latex_template % text
        # TODO: clean it up using markdown to latex
        chapter_re = re.compile('Chapter (.*)')
        final = chapter_re.sub(r'\chapter{\1}', final)
        latex_path = localpath + '.tex'
        open(latex_path, 'w').write(final)
        # now build it
        builddir = self.cache.path('build')
        if not os.path.exists(builddir):
            os.makedirs(builddir)
        cmd = 'pdflatex --output-dir=%s %s' % (builddir, latex_path)
        os.system(cmd)

if __name__ == '__main__':
    import sys
    # url = sys.argv[1]
    pdfator = Pdfator('/tmp/pdfator')
    # dameaux = 'http://www.gutenberg.org/dirs/etext00/8dame10.txt'
    dameaux = 'http://www.gutenberg.org/files/1608/1608.txt'
    pdfator.execute(dameaux)

