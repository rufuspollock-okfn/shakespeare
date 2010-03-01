from __future__ import division
import string,nltk
from nltk.corpus import wordnet as wn
import operator

'''
Several different scripts to analyze the
xml versions of Shakespeare plays
by Jon Bosak
http://www.cafeconleche.org/examples/shakespeare/
'''


print 'please run \nfrom nltk.book import  *\n '

lines = open('text.txt','rU').readlines()
austenpersuasion = nltk.corpus.gutenberg.words('austen-persuasion.txt')
alice = nltk.corpus.gutenberg.words('carroll-alice.txt')


smallcaps = lambda n: string.lower(n)

def shakespeare_words_in_books():    
    for book in nltk.corpus.shakespeare.fileids():
        print book + ':', len(nltk.corpus.shakespeare.words(book))


def mainnoundict(wordlist):
    """
    the nltk library has a function, FDist, that does this and more:
    fdist1 = FreqDist(text2)
    fdist1.freq('the')

    """ 
    nounslist = {}
    for i in wordlist:
        is_noun = lambda i: wn.synsets(i, pos=wn.NOUN)
        if ( wn.synsets(i, pos=wn.NOUN)!=''):
	    if i in nounslist:
		if i not in [',','"',';','\'','.']:
        	    nounslist[i]=nounslist[i]+1
	    else:
		nounslist[i]=1
    for i in nounslist:
        if ( wn.synsets(i , pos=wn.VERB)):
		i
    return nounslist

def top_ten_words(nounslist):

    dictwords = mainnoundict(nounslist) 
    result = sorted(list(dictwords.items()), key=operator.itemgetter(1))
    return result
 
def percentage_on_text(text,word):
    """ gives the percentage of word occurences in text """
    return 100 * text.count(word) / len(text)

def words_variety(text):
    return len(text) / len(set(text))

def compare_word_varieties(corpus):
    texts = {}
    for text in corpus:
        texts[text] = words_variety(text)
        if len(text)>5:
            print text.items()
            #    return texts



def analyze_text(text):

    frdis = nltk.FreqDist(text)
    freqlongwords = {} 
    names = {}
    for i,value in set(frdis.items()):
        if i.istitle() and i.isalpha():
            names[i] = value
        if len(i) > 8 and value > 10:
            freqlongwords[i] = value
            #print i, value
    uniquewords = len(frdis.hapaxes())


    print "\ntotal of words", len(text)
    print "\nfrequency distribution ", len(frdis)
    print "\nuniquewords ", uniquewords
    print "\ncollocations: ", text.collocations()
    print len(freqlongwords.items()), "\nwords longer than 8 characters that appear more than 9 times" , freqlongwords.items()[-10:] 
    print "some names: " , names.items()[:13]


def corpusnumbers(corpus):

    for fileid in corpus.fileids():
        num_chars = len(corpus.raw(fileid))
        num_words = len(corpus.words(fileid))
        num_sents = len(corpus.sents(fileid))
        num_vocab = len(set([w.lower() for w in corpus.words(fileid)]))
        print int(num_chars/num_words),  int(num_words/num_sents),  int(num_words/num_vocab),fileid
        

def wordsplot(words,text):
    ''' 
    Given a list of words and a text, makes a plot with the frequency distribution of the words
    '''
    vocab = sorted(set(text))
    word_freq = nltk.FreqDist(text)
    cfd = nltk.ConditionalFreqDist(
        (oneword, freq )
        for oneword in vocab
        for freq in words)

    cfd.tabulate(cumulative=True)
    cfd.plot(cumulative=True)

def unusual_words(text):
    from nltk.corpus import stopwords
    text_vocab = set(w.lower() for w in text if w.isalpha())
    common_words = stopwords.words('english')
    unusual = text_vocab.difference(common_words)
    content = [w for w in set(text) if w.lower() not in common_words]
    #    return len(unusual)
    print "\nunusual words: ", len(unusual), " of ", len(text_vocab), " words","\nother unusual calculation: ",len(content),"\ncommon words: ",len(common_words)
