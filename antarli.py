"""
Author: Amogh Jalihal 
Commentary: Map hex codes for unicode
character across Indic scripts to convert an input string into a user
specified language script. This is NOT a translation tool.

This set of Unicode character limiters are derived from
https://symbl.cc/en/unicode/table

Indic languages are defined over 127 characters, and each script specific
character set is organized to retain the same structure. It is thus trivial
to offset the hex codes to transliterate from one script to the other.

Note: Because Tamizh has fewer characters than others, many characters will not
get meaningfully mapped and will fail to render.
| language   | unicode_start | unicode_end |
|------------+---------------+-------------|
| Devanagari | 0900          | 097F        |
| Bengali    | 0980          | 09FF        |
| Gurmukhi   | 0A00          | 0A7F        |
| Gujarati   | 0A80          | 0AFF        |
| Oriya      | 0B00          | 0B7F        |
| Tamil      | 0B80          | 0BFF        |
| Telugu     | 0C00          | 0C7F        |
| Kannada    | 0C80          | 0CFF        |
| Malayalam  | 0D00          | 0D7F        |
"""
from ast import literal_eval
import streamlit as st
import clipboard

r= [["देवनागरी", "0900", "097F"], 
   ["বাংলা", "0980", "09FF"], 
    ["ਗੁਰਮੁਖੀ", "0A00", "0A7F"], 
    ["ગુજરાતી", "0A80", "0AFF"], 
    ["ଓଡ଼ିଆ", "0B00", "0B7F"], 
    ["தமிழ்", "0B80", "0BFF"], 
    ["తెలుగు", "0C00", "0C7F"],
    ["ಕನ್ನಡ", "0C80", "0CFF"], 
    ["മലയാളം", "0D00", "0D7F"]]





def dec2hex(d):
    return(hex(d))

def hex2dec(h):
    return(literal_eval(h))

def hex2unicode(h):
    return((br"\u" + h.replace("0x","").rjust(4,"0").encode('utf-8')).decode('unicode_escape'))

def unicode2hex(u):
    return(format(ord(u), '#08x'))

def get_scripts(s):
    """
    For every unicode character, map back to encoding space to retrieve the script name.
    """
    lang = []
    for c in s:
        for l, (s, e) in unicode_space.items():
            val = hex2dec(unicode2hex(c)) 
            if (val >= s) and (val <= e):
                lang.append(l)
                lang = list(set(lang))
    return(lang)

def on_copy_click(text):
    clipboard.copy(text)

def convert_to_target(string, target):
    """
    Accepts a string and a target language
    """
    newstring = ""
    for char in string:
        if char == " ":
            newstring += char
        else:
            found = False
            for l, (s, e) in unicode_space.items():
                val = hex2dec(unicode2hex(char)) 
                if (val >= s) and (val <= e):
                    found = True
                    break
            if found:
                offset = hex2dec(unicode2hex(char)) - s

                try:
                    newchar = hex2unicode(dec2hex(unicode_space[target][0] + offset))
                except:
                    print(newchar)
                newstring += newchar
            else:
                newstring += char
    return(newstring)    

unicode_space = {}
for row in r:
    lang, start, end = row
    if len(str(start)) == 3:
        start, end = str(start).rjust(4,"0"),str(end).rjust(4,"0")
    unicode_space[lang] = (literal_eval("0x" + start),
                     literal_eval("0x" + end))
# basic utilities:1 ends here


# for lang, (start, end) in unicode_space.items():
#     print(lang)
#     for i in range(start, start + 2):
#         print(i, dec2hex(i), hex2unicode(dec2hex(i)), unicode2hex(hex2unicode(dec2hex(i))), hex2dec(unicode2hex(hex2unicode(dec2hex(i)))))


page = st.sidebar.selectbox("Navigate", ["AntarLipy","About"])

if page == "AntarLipy":
    st.title("AntarLi.py")
    st.markdown("## Render Indic text in your favorite script!")
    
    col1, col2 = st.columns(2)

    with col1:
        #st.header("Input Text")
        inputstring = st.text_area("Please enter text\n(on mobile, tap anywhere outside the text box when you are done)", "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः")
        
    lang = get_scripts(inputstring)
    if len(lang) == 1:
        st.markdown(f"`detected {lang[0]}`")
    else:
        st.markdown(f"`detected multiple scripts: {lang}`")

    with col2:
        target = st.selectbox("Render in", unicode_space.keys())
        converted = convert_to_target(inputstring, target)
        # st.button("Copy to clipboard 📋", key="copy",on_click=on_copy_click, args=(converted,))
        st.markdown(converted)
else:
    st.title("Welcome to AntarLi.py!")
    st.markdown("This tool was built by [Amogh Jalihal](https://amoghjalihal.com). \n\nYou can find the source code here: https://github.com/amoghpj/antarli.py\n\nAlways happy to implement new features, so leave a note with any suggestions and feedback!")
