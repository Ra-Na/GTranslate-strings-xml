#!/usr/bin/env python
# -*- coding: utf-8 -*-


XMLINFILE='teststrings.xml'
STRINGINFILE='teststrings_translated.txt'
OUTFILE='teststrings_de.xml'

import xml.etree.ElementTree as ET
import re

# http://stackoverflow.com/questions/33573807/faithfully-preserve-comments-in-parsed-xml-python-2-7
class CommentedTreeBuilder(ET.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

#------------------------------------------------------------------------------
cparser = ET.XMLParser(target = CommentedTreeBuilder())
def read_xml_file(f):
    return ET.parse(f, parser=cparser)

# prepare things
#tree = ET.parse(XMLINFILE)
tree = read_xml_file(XMLINFILE)
root = tree.getroot()
file = open(STRINGINFILE,'r') 
translations=file.readlines();
file.close()


#~ for i in range(len(translations)):
    #~ param, value = translations[i].split(":",1)
    #~ root[i].text=value

    
counter=0
p=re.compile('^[\d]*:.*')
translationLines=len(translations)-1
for i in range(len(root)):
    isTranslatable=root[i].get('translatable')
    if(root[i].tag=='string') & (isTranslatable!='false'):
        counter=counter+1
        param, value = translations[counter-1].split(":",1)
        if(counter<translationLines):
            while True:
                counter=counter+1
                if(counter>translationLines) | (p.match(translations[counter-1])!=None):
                    counter=counter-1
                    break
                else:
                    value = value + translations[counter-1]
        root[i].text=value.rstrip()
    else:
        if(root[i].tag=='string-array') & (isTranslatable!='false'):
            for j in range(len(root[i])):	
                if(root[i][j].tag=='item'):
                    counter=counter+1
                    multiLine=False
                    param, value = translations[counter-1].split(":",1)
                    if(counter<translationLines):
                        while True:
                            counter=counter+1
                            if(counter>translationLines) | (p.match(translations[counter-1])!=None):
                                counter=counter-1
                                break
                            else:
                                multiLine=True
                                value = value + translations[counter-1]
                    # fix incorrect addition of fullstop by translation service.
                    value.replace('".','"')
                    # remove spurious added newlines
                    if(multiLine):
                        if(len(value)>1) & (value[-1:] == '\n'):
                            value=value[:-1]
                        root[i][j].text=value
                    else:
                        root[i][j].text=value.rstrip()
tree.write(OUTFILE, encoding='utf-8')
