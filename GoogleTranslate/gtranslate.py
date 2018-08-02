#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This python skript extracts string resources, calls Google translate
# and reassambles a new strings.xml as fitted for Android projects.

# run via "python3.5 gtranslate.py", newer versions should work as well

### Settings 

INPUTLANGUAGE='en'
OUTPUTLANGUAGE='th'
INFILE='teststrings.xml'
OUTFILE='teststrings_th.xml'

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
#   tn          Setswana
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

import html
import requests
import os
import xml.etree.ElementTree as ET
from io import BytesIO

def translate(to_translate, to_language="auto", language="auto"):
 r = requests.get("http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_language, language, to_translate.replace(" ", "+")))
 beforecharset='charset='
 aftercharset='" http-equiv'
 parsed1=r.text[r.text.find(beforecharset)+len(beforecharset):]
 parsed2=parsed1[:parsed1.find(aftercharset)]
 
 if(parsed2!=r.encoding):
     print('\x1b[1;31;40m' + 'Warning: Potential Charset conflict' )
     print(" Encoding as extracted by SELF    : "+parsed2)
     print(" Encoding as detected by REQUESTS : "+r.encoding+ '\x1b[0m')

# Work around an AGE OLD Python bug in case of windows-874 encoding
# https://bugs.python.org/issue854511

 if(r.encoding=='windows-874' and os.name=='posix'):
     print('\x1b[1;31;40m' + "Alert: Working around age old Python bug (https://bugs.python.org/issue854511)\nOn Linux, charset windows-874 must be labeled as charset cp874"+'\x1b[0m')
     r.encoding='cp874'

 text=html.unescape(r.text)    
 before_trans = 'class="t0">'
 after_trans='</div><form'
 parsed1=r.text[r.text.find(before_trans)+len(before_trans):]
 parsed2=parsed1[:parsed1.find(after_trans)]
 print(parsed2) 
 return html.unescape(parsed2)



tree = ET.parse(INFILE)
root = tree.getroot()
for i in range(len(root)):
    isTranslatable=root[i].get('translatable')
    print((str(i)+" ========================="))
    if(isTranslatable=='false'):
        print("Not translatable")
    if(root[i].tag=='string') & (isTranslatable!='false'):
        totranslate=root[i].text
        print(totranslate)
        print("-->")
        if(totranslate!=None):
            root[i].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE)
            print(root[i].text)
    if(root[i].tag=='string-array'):
        print("Entering string array...")
        for j in range(len(root[i])):
            isTranslatable=root[i][j].get('translatable')
            print((str(i)+" "+str(j)+" ========================="))
            if(isTranslatable=='false'):
                print("Not translatable")
            if(root[i][j].tag=='item') & (isTranslatable!='false'):
                totranslate=root[i][j].text
                print(totranslate)
                if(totranslate!=None):
                    root[i][j].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE)
                    print(root[i][j].text)
     
tree.write(OUTFILE, encoding='utf-8')

