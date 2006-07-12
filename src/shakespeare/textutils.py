import shakespeare.utils

def get_snippet(fileobj, charIndex, neighbourhood=30):
    # always get the cleaned version (since that is what concordancer uses
    ss = fileobj.read()
    start = max(0, charIndex - neighbourhood)
    # add some extra to take account that charIndex is from start of word
    extra = 8
    end = min(len(ss), charIndex + neighbourhood + extra)
    return '...' + ss[start:end].strip() + '...'
