import os

cmdbase = 'rsync -avz %s okfn@openshakespeare.org:~/var/srvc/openshakespeare.org/%s'
html = 'cache/moby/html/'
htmlcmd = cmdbase % (html, html)
pdf = 'cache/moby/pdf/'
pdfcmd = cmdbase % (pdf, pdf)

print htmlcmd
os.system(htmlcmd)

print pdfcmd
os.system(pdfcmd)

