#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# This python skript extracts string resources from a XML file and
# puts them into a text file with a unique header/string delimiter. 
# This may be copy-pasted
# to a translation engine, a similar Python program then reverses
# the strings into the xml file, assuming that the string delimiter 
# is not affected by the translation. 
# The output is send to stdout, append pipes (like " >> mystrings.txt" 
# to send to a file.

# run via 

# PYTHONIOENCODING=utf8 python3.5 dx2t.py strings.xml "::"

# where firstly the environment variable PYTHONENCODING is set,
# then python is called,
# then the name of the current file plus argument strings, 
# where the first argument is the xml input file and
# the second argument is the unique delimiter that should be used.

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

#
#   SUBROUTINES
#

# This subroutine extracts the string including html tags
# and may replace "root[i].text".  
# It cannot digest arbitrary encodings, so use it only if necessary.
def findall_content(xml_string, tag):
    pattern = r"<(?:\w+:)?%(tag)s(?:[^>]*)>(.*)</(?:\w+:)?%(tag)s" % {"tag": tag}
    return re.findall(pattern, xml_string, re.DOTALL)

#
# MAIN PROGRAM
#

# import libraries
import xml.etree.ElementTree as ET
import sys
import re

# read xml structure
tree = ET.parse(sys.argv[1])
root = tree.getroot()

# set delimiter
delim=sys.argv[2]
counter=0
    
for i in range(len(root)):
#	extract each translatable string,
#   descend into each string array  
    isTranslatable = root[i].get('translatable')
    if(root[i].tag=='string') & (isTranslatable!='false'):
# Here you might want to replace root[i].text by the findall_content function
# if you need to extract html tags
        # ~ ste="".join(findall_content(str(ET.tostring(root[i])),"string"))
        counter = counter + 1
        ste=root[i].text
        print(str(counter)+delim+ste)
    if(root[i].tag=='string-array') & (isTranslatable!='false'):
        for j in range(len(root[i])):	
            if(root[i][j].tag=='item'):
                isTranslatable = root[i][j].get('translatable')
                if(isTranslatable!='false'):
# Here you might want to replace root[i].text by the findall_content function
# if you need to extract html tags
                    # ~ ste="".join(findall_content(str(ET.tostring(root[i][j])),"item"))
                    counter = counter + 1
                    ste=root[i][j].text
                    print(str(counter)+delim+ste)

