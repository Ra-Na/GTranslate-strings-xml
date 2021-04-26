#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This python skript extracts string resources, calls Google translate
# and reassambles a new strings.xml as fitted for Android projects.

# run via 

# PYTHONIOENCODING=utf8 python3 gtranslate.py  OR using pythong launcher 
# follow instructions

# output format: values-XX folders with strings.xml inside

# edited by alexVinrskis, March 2020

### LANGUAGE CODES FOR REFERENCE

#   af          Afrikaans
#   ak          Akan
#   sq          Albanian
#   am          Amharic
#   ar          Arabic
#   hy          Armenian
#   az          Azerbaijani
#   eu          Basque
#   be          Belarusian
#   bem         Bemba
#   bn          Bengali
#   bh          Bihari
#   xx-bork     Bork, bork, bork!
#   bs          Bosnian
#   br          Breton
#   bg          Bulgarian
#   km          Cambodian
#   ca          Catalan
#   chr         Cherokee
#   ny          Chichewa
#   zh-CN       Chinese (Simplified)
#   zh-TW       Chinese (Traditional)
#   co          Corsican
#   hr          Croatian
#   cs          Czech
#   da          Danish
#   nl          Dutch
#   xx-elmer    Elmer Fudd
#   en          English
#   eo          Esperanto
#   et          Estonian
#   ee          Ewe
#   fo          Faroese
#   tl          Filipino
#   fi          Finnish
#   fr          French
#   fy          Frisian
#   gaa         Ga
#   gl          Galician
#   ka          Georgian
#   de          German
#   el          Greek
#   gn          Guarani
#   gu          Gujarati
#   xx-hacker   Hacker
#   ht          Haitian Creole
#   ha          Hausa
#   haw         Hawaiian
#   iw          Hebrew
#   hi          Hindi
#   hu          Hungarian
#   is          Icelandic
#   ig          Igbo
#   id          Indonesian
#   ia          Interlingua
#   ga          Irish
#   it          Italian
#   ja          Japanese
#   jw          Javanese
#   kn          Kannada
#   kk          Kazakh
#   rw          Kinyarwanda
#   rn          Kirundi
#   xx-klingon  Klingon
#   kg          Kongo
#   ko          Korean
#   kri         Krio (Sierra Leone)
#   ku          Kurdish
#   ckb         Kurdish (Soranî)
#   ky          Kyrgyz
#   lo          Laothian
#   la          Latin
#   lv          Latvian
#   ln          Lingala
#   lt          Lithuanian
#   loz         Lozi
#   lg          Luganda
#   ach         Luo
#   mk          Macedonian
#   mg          Malagasy
#   ms          Malay
#   ml          Malayalam
#   mt          Maltese
#   mi          Maori
#   mr          Marathi
#   mfe         Mauritian Creole
#   mo          Moldavian
#   mn          Mongolian
#   sr-ME       Montenegrin
#   ne          Nepali
#   pcm         Nigerian Pidgin
#   nso         Northern Sotho
#   no          Norwegian
#   nn          Norwegian (Nynorsk)
#   oc          Occitan
#   or          Oriya
#   om          Oromo
#   ps          Pashto
#   fa          Persian
#   xx-pirate   Pirate
#   pl          Polish
#   pt-BR       Portuguese (Brazil)
#   pt-PT       Portuguese (Portugal)
#   pa          Punjabi
#   qu          Quechua
#   ro          Romanian
#   rm          Romansh
#   nyn         Runyakitara
#   ru          Russian
#   gd          Scots Gaelic
#   sr          Serbian
#   sh          Serbo-Croatian
#   st          Sesotho
#   tn          Setswanadef findall_content(xml_string, tag):

#   crs         Seychellois Creole
#   sn          Shona
#   sd          Sindhi
#   si          Sinhalese
#   sk          Slovak
#   sl          Slovenian
#   so          Somali
#   es          Spanish
#   es-419      Spanish (Latin American)
#   su          Sundanese
#   sw          Swahili
#   sv          Swedish
#   tg          Tajik
#   ta          Tamil
#   tt          Tatar
#   te          Telugu
#   th          Thai
#   ti          Tigrinya
#   to          Tonga
#   lua         Tshiluba
#   tum         Tumbuka
#   tr          Turkish
#   tk          Turkmen
#   tw          Twi
#   ug          Uighur
#   uk          Ukrainian
#   ur          Urdu
#   uz          Uzbek
#   vi          Vietnamese
#   cy          Welsh
#   wo          Wolof
#   xh          Xhosa
#   yi          Yiddish
#   yo          Yoruba
#   zu          Zulu

#
#   SUBROUTINES
#

# This subroutine calls Google translate and extracts the translation from
# the html request
def translate(to_translate, to_language="auto", language="auto"):
    # send request
    r = requests.get("https://translate.google.com/m?sl=%s&tl=%s&q=%s&op=translate"% (language, to_language, to_translate.replace(" ", "+")))	
    beforecharset = 'charset='
    aftercharset = '" http-equiv'
    # extract charset 
    parsed1 = r.text[r.text.find(beforecharset) + len(beforecharset):]
    parsed2 = parsed1[:parsed1.find(aftercharset)]
    # Display warning when encoding mismatch 
    if (parsed2 != r.encoding):
        print('\x1b[1;31;40m' + 'Warning: Potential Charset conflict')
        print(" Encoding as extracted by SELF    : " + parsed2)
        print(" Encoding as detected by REQUESTS : " + r.encoding + '\x1b[0m')
    
    # Work around an AGE OLD Python bug in case of windows-874 encoding
    # https://bugs.python.org/issue854511
    if (r.encoding == 'windows-874' and os.name == 'posix'):
        print(
            '\x1b[1;31;40m' + "Alert: Working around age old Python bug (https://bugs.python.org/issue854511)\nOn Linux, charset windows-874 must be labeled as charset cp874" + '\x1b[0m')
        r.encoding = 'cp874'
    
    # convert html tags  
    text = html.unescape(r.text)
    # set markers that enclose the wanted translation
    before_trans = 'class="result-container">'
    after_trans = '</div>'
    # extract translation and return it
    parsed1 = r.text[r.text.find(before_trans) + len(before_trans):]
    parsed2 = parsed1[:parsed1.find(after_trans)]
    # fix parameter strings
    parsed3 = re.sub('% ([ds])', r' %\1', parsed2)
    parsed4 = re.sub('% ([\d]) \$ ([ds])', r' %\1$\2', parsed3).strip()
    return html.unescape(parsed4).replace("'", r"\'")



# MAIN PROGRAM

# import libraries
import html
import requests
import os
import xml.etree.ElementTree as ET
import sys
from io import BytesIO
import re
import time

# ask user for paramters, apply defaults
INFILE = input("Enter input filename: [default: strings.xml]\n")
INPUTLANGUAGE = input("\nEnter source language: [default: en]\n")
OUTPUTlangs = input("\nEnter output language(s): (space separated) \n\n").split()
if not INFILE:
    INFILE = "strings.xml"
if not INPUTLANGUAGE:
    INPUTLANGUAGE = "en"

print("=================================================\n\n")

# repeat proccess for each of the lang 
for OUTPUTLANGUAGE in OUTPUTlangs:
    OUTFILE= "strings_"+OUTPUTLANGUAGE+".xml"
    # read xml structure
    tree = ET.parse(INFILE)
    root = tree.getroot()

    print(OUTPUTLANGUAGE + "...\n")

    # cycle through elements 
    for i in range(len(root)):
    #	for each translatable string call the translation subroutine
    #   and replace the string by its translation,
    #   descend into each string array  
        time.sleep(1)
        isTranslatable=root[i].get('translatable')
        if(root[i].tag=='string') & (isTranslatable!='false'):
            # trasnalte text and fix any possible issues traslotor creates: messing up HTML tags, adding spaces between string formatting elements
            totranslate=root[i].text
            if(totranslate!=None):
                root[i].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')

            # if string was broken down due to HTML tags, reassemble it
            if len(root[i]) != 0:
                for element in range(len(root[i])):
                    root[i][element].text = " " + translate(root[i][element].text, OUTPUTLANGUAGE, INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')
                    root[i][element].tail = " " + translate(root[i][element].tail, OUTPUTLANGUAGE, INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')

        if(root[i].tag=='string-array'):
            for j in range(len(root[i])):
    #	for each translatable string call the translation subroutine
    #   and replace the string by its translation,
                isTranslatable=root[i][j].get('translatable')
                if(root[i][j].tag=='item') & (isTranslatable!='false'):
                    # trasnalte text and fix any possible issues traslotor creates: messing up HTML tags, adding spaces between string formatting elements
                    totranslate=root[i][j].text
                    if(totranslate!=None):
                        root[i][j].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')

                    # if string was broken down due to HTML tags, reassemble it
                    if len(root[i][j]) != 0:
                        for element in range(len(root[i][j])):
                            root[i][j][element].text = " " + translate(root[i][j][element].text, OUTPUTLANGUAGE, INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')
                            root[i][j][element].tail = " " + translate(root[i][j][element].tail, OUTPUTLANGUAGE, INPUTLANGUAGE).replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')

    # write new xml file
    tree.write(OUTFILE, encoding='utf-8')

