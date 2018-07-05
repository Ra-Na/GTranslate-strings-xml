#!/usr/bin/env python
# -*- coding: utf-8 -*-


XMLINFILE='teststrings.xml'
STRINGINFILE='teststrings_translated.txt'
OUTFILE='teststrings_de.xml'

import xml.etree.ElementTree as ET

# prepare things
tree = ET.parse(XMLINFILE)
root = tree.getroot()
file = open(STRINGINFILE,'r') 
translations=file.readlines();
file.close()


#~ for i in range(len(translations)):
    #~ param, value = translations[i].split(":",1)
    #~ root[i].text=value

    
counter=0    
for i in range(len(root)):
    if(root[i].tag=='string'):
        counter=counter+1
        param, value = translations[counter-1].split(":",1)
        root[i].text=value         
    if(root[i].tag=='string-array'):
        for j in range(len(root[i])):	
            if(root[i][j].tag=='item'):
                counter=counter+1
                param, value = translations[counter-1].split(":",1)
                root[i][j].text=value         
    
tree.write(OUTFILE, encoding='utf-8')
