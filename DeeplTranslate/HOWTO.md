
How to use DEEPL.COM to translate Android string resource XML files.

* Why? 

Deepl.com offers higher quality translations than translate.google.com 
between FRENCH, GERMAN, ENGLISCH, DUTCH, ITALIAN, SPANISH and POLISH.

* How? 

Non-commercial use is restricted to explicitely clicking on the website,
automated HTML-requests are available as a payed service only. 

Therefore:

1. `python3.6 dx2t.py teststrings_de.xml "::" >> "out.txt"` extracts all strings to a text file named `out.txt`.
2. Copy-paste the text file's content on the DEEPL.COM website or any other translation engine of your choice.
3. Copy-paste the result to another text file, here `out_trans.txt`. Make sure that the delimiters and line numbers are not messed up by the translation service. 
4. `python3.6 dt2x.py teststrings_de.xml out_trans.txt "::"` puts the translated strings into a 
    new XML file. 
   
It is important that both Python files get the XML structure from the same 
input file.

This works at [asrt.gluege.boerde.de](asrt.gluege.boerde.de) behind a web page.
