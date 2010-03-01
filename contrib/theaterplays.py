import nltk

'''
Several different scripts to analyze the
xml versions of Shakespeare plays
by Jon Bosak
'''


def character_speech(xmlplay):
    '''
    Given an xml shakespeare file,
    separates the text of the different characters 
    on the play
    '''
    xml = nltk.corpus.shakespeare.xml(xmlplay)
    characters = xml.getiterator('PERSONAE')
    bycharacter = {}
    text = xml.getiterator('SPEECH')

    for intervention in text:
        character = intervention.get('SPEAKER')
        speech = intervention.getiterator('LINE')


    new = []
    for i in xml.getiterator():
        if i.text and i.tag == 'SPEAKER':
            char = i.text

        if i.text and i.tag == 'LINE':
            mytext = i.text
            new.append([char,mytext])
    return new
    #print(new)

def get_text(xmlplay):
    '''
    loads a shakespeare xml file and returns a dictionary in the form of 
    {charachter: ['tokenized','text']}
    '''
    xml = nltk.corpus.shakespeare.xml(xmlplay)
    new = {}
    for i in xml.getiterator():

        # detect characters
        if i.text and i.tag == 'SPEAKER':
            char = i.text
            if char not in new.keys():
                new[char]=[]
        # detect words
        if i.text and i.tag == 'LINE':
            mytext = i.text
            for word in nltk.wordpunct_tokenize(mytext):
                new[char].append(word)
    return new


def smallcharacteranalysis(xmlplay):
    '''
    Loads a Shakespeare xml file (Bosak) and makes calculations
    on the characters
    '''
    textinfo = {}
    new = get_text(xmlplay)
    xml = nltk.corpus.shakespeare.xml(xmlplay)
    
    textinfo['numberofchars'] = len(new)
    textinfo['wordsperchar'] = [ (char, len(lines)) for char,lines in new.items() ]
    #print new.items()
    textinfo['yes'] = []
    textinfo['no'] = []
    textinfo['charlist'] = []
    textinfo['hapaxes'] = [] 
    textinfo['vocab'] = []
    textinfo['length_list'] = []
    textinfo['questionmarks'] = []
    textinfo['exclammarks'] = []
    textinfo['book'] = new
    textinfo['postags'] = {}
    for char, words in new.items():
        if char.isupper() and len(words)>100:
            textinfo['charlist'].append(char)
            fdist = nltk.FreqDist(words)
            textinfo['hapaxes'].append(len(fdist.hapaxes()))
            textinfo['vocab'].append(len(fdist)-len(fdist.hapaxes()))
            textinfo['length_list'].append(len(words)-len(fdist))
            textinfo['yes'].append( fdist.freq('yes')+fdist.freq('Yes'))
            textinfo['no'].append( fdist.freq('no')+fdist.freq('No'))
            textinfo['questionmarks'].append( fdist.freq('?'))
            textinfo['exclammarks'].append( fdist.freq('!'))
    return textinfo
        

def pos_per_char(words):
    '''
    Loads a tokenized list of words like ['The', 'house', 'is' ]  and creates a list of tuples in the form
    of [('The','NP'), ('house','NN'),('is'),('VP)...] for further processing.
    Lots of CPU use!
    '''

    withloc = nltk.pos_tag(words)
    fdist = nltk.FreqDist([word for word, tag in withloc if tag not in ['.',',',';','"','?','\''] and tag !=  'NP'])
    types = nltk.FreqDist(tag for word, tag in withloc)
    pronouns = set([word for word, tag in withloc if tag == 'PRP'])
    nouns = set([word for word, tag in withloc if tag.startswith('NN') and fdist.freq('word')>4])
    info = {'pos_words': withloc, 'pronouns': pronouns, 'pos types': types.items(), 'fdist': fdist, 'nouns': nouns }

    return info
    

def modalsbycharacter(words):
    '''
    takes a dictionary {charachter: ['tokenized','text']} and plots the
    conditional verbs per character if they say more than 100 lines
    '''
    conditionals = nltk.defaultdict(dict)
    try:
        for char, text in words.items():
            tagged = nltk.pos_tag(text)
            conditionals[char] =  nltk.FreqDist(
                [positionedword for positionedword,
                tag in tagged if tag == 'MD']).items()  

        return conditionals
    except AttributeError:
        print 'please enter a dictionary in the form of {charachter: ['tokenized','text']} '

def modalsmap(words,conditionals):
    '''
    given a speech list in the form of {'YOUNG SIWARD': ['What', 'is','thy',
    'name','?'], } creates a graphviz map of conditionals per (important)
    character
    '''
    import pydot

    all = []
    for char, words in conditionals.items():
        for word in words:
            all.append((char,word[0].lower()))

            
    graphic = pydot.graph_from_edges(all)
    for char in conditionals:
        new = pydot.Node(char,color='green',shape='doubleoctagon',fontname='Arial',fontsize='12',rank='source', ranksep = '1.2')
        graphic.add_node(new)
    for char, word in all:
        new = pydot.Node(word,color='purple',shape='note',fontname='Arial',fontsize='8')
        graphic.add_node(new)


    graphic.set_overlap('TRUE')
    graphic.set_splines('True')
    graphic.set_suppress_disconnected('TRUE')
    graphic.write_png('/tmp/test.png',prog='twopi')





def characters(xmlplay):
    '''
    Loads a Shakespeare xml file (Bosak) and makes calculations
    on the characters
    Creates a small index.html file with a google chart
    '''
    book = smallcharacteranalysis(xmlplay)
    
    from graphy.backends import google_chart_api
    from graphy import line_chart


        #pass
    # Lexical diversity BarChart
    chart = google_chart_api.BarChart()
    chart.AddBars(book['hapaxes'], color='a06F00',label='words said just once')
    chart.AddBars(book['vocab'], color='506F00',label='repeated words')
    chart.AddBars(book['length_list'], color='006F00',label='repetitions of the repeated words')
    chart.vertical = False
    chart.stacked = True
    #chart.auto_legend()
    chart.bottom.min = 0
    chart.left.labels = book['charlist']
    chart.left.max = len(book['charlist'])+1
    chart.left.min = 0
    chart.left.label_positions = [range(len(book['charlist']))]

    #chart.bottom.labels = char_list

    #Pie Chart total words

    pie = google_chart_api.PieChart(book['length_list'],book['charlist'])
    

    #line chart ? and !
    exxageration = google_chart_api.BarChart()
    exxageration.AddBars(book['exclammarks'], color='a06F00',label='Exclamation Marks('!')')
    exxageration.AddBars(book['questionmarks'], color='506F00',label='Question Marks ('?')')
    exxageration.vertical = False
    exxageration.left.labels = book['charlist']
    exxageration.bottom.min = 0
    exxageration.left.labels = book['charlist']
    exxageration.left.max = len(book['charlist'])+1
    exxageration.left.min = 0
    exxageration.left.label_positions = [range(len(book['charlist']))]



    import os.path
    file = 'index.html'
    infile = open(file,'w')
    infile.write('<h2>Lexical Variety</h2>')
                 
    infile.write(chart.display.Img(600, 400))
    
    infile.write('<h2>All words spoken, totals per character</h2>')
    infile.write(pie.display.Img(600, 300))

    infile.write('<h2>Exageration and questioning</h2>')
    infile.write(exxageration.display.Img(600, 300))

def newmap(words):
    ''' 
    takes a series  {charachter: ['tokenized','text']} 
    and plots it in different ways with networkx
    '''
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(text.keys(),color='#ff33cc',size='20')
        
