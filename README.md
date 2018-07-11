# GTranslate-strings-xml
# DTranslate-strings-xml

This is a FORKED Repository: Why?

This has been forked from Ra-Na original project. I did this because I couldn't obviously see how to push my enhancements to their repository.

This adds support above this in the original project as follows:
1. Support for translatable=false
2. Support to copy across comments verbatim
3. Bugs exist as in the original as of 11th July 2018:
    * &lt;![CDATA[some stuff]]> tag is corrupted
    * &gt; is converted to url safe &amp;gt;
    * content type header is stripped from file

ORIGINAL README Content below:


Provides python3.5 scripts that automate string resource file translations as needed for Android projects.
As of July 2018, two translation services are implemented, namely DEEPL and GOOLGE TRANSLATE.

Note:

1.) For English
        German
        Italian
        French
        Spanish
        Dutch
        Polish Deepl yields better translations. 
        
2.) The Google translate script should by now handle asian fonts correctly.
   
