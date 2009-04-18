from itertools import groupby

import re

from xml.dom.minidom import Document

text = open('C:\\texts\\midsummer_nights_dream_gut.txt').read()

#Still need to deal with attaching 

def paragraphs(lines, is_separator=str.isspace, joiner=''.join):
    for separator_group, lineiter in groupby(lines, key=is_separator):
        if not separator_group:
            yield joiner(lineiter)

def scene_node(scene):
    global docText
    docText = doc.createElement("div")
    #need to set the type to book, verse, drama
    docText.setAttribute("type", "scene")
    #need set the id to what ever break name or id: i.e. chapter 1 or act 1
    docText.setAttribute("id", ' ')
    tei.appendChild(docText)
    for acts in scene.split('ACT'):
        act_node(acts)

    return docText

def act_node(act):
    global actText
    actText = doc.createElement("div")
    #need to set the type to book, verse, drama
    actText.setAttribute("type", "act")
    #need set the id to what ever id: 1 or I
    actText.setAttribute("id", ' ')
    docText.appendChild(actText)
    for p in paragraphs(act.splitlines(True)):
        speech_node(p)

    return actText

def speech_node(speech):
    #still need an if to ignore the stage directions and add them to a different tag
    para = doc.createElement("p")
    actText.appendChild(para)
    ptext = doc.createTextNode(speech)
    para.appendChild(ptext)
    return speech
    

doc = Document()
tei = doc.createElement("body")
doc.appendChild(tei)
front_matter = doc.createElement("front")
#need to identify all material before the first scene
# and make sure it isn't called later. 
tei.appendChild(front_matter)

#probably needs changing to a regex: something like (?=SCENE)
for textStr in text.split('SCENE'):
    scene_node(textStr)

print doc.toprettyxml(indent = " ")

