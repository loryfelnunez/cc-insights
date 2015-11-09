"""
Library of functions for cleaning text and extracting elements from text
List of functions:
    - convert_to_date
    - is_only_punct
    - get_hash_tags
    - replace_escape_chars
    - strip_non_ascii
    
Created on Fri Nov 6 05:03:17 2015
@author: Loryfel T. Nunez
"""

import re
import json
import datetime
import dateutil.parser
import string


def convert_to_date(text):
    """ Returns a date object from a text representation """
    return dateutil.parser.parse(text)

def is_only_punct(text):
    """ Check if remaining text contains only punctuation """
    in_text = text.replace(" ", "")
    puncs = set(string.punctuation)
    chars = [i for i in in_text if all(j in puncs for j in in_text)]
    return True if len(chars) > 0 else False
      
    
def get_hash_tags(text):
    """ Returns a deduped set of twitter hash tags """
    words = text.split(' ')
    return set([w.upper() for w in words if w.startswith('#')])

def replace_escape_chars(text):
    """ Returns translations of escaped characters """
    DictionaryReplace = {"\/":"/", "\\\\":"\\", "\\'":"\'", "\n":" ", "\t":" ", "\r":" "}
    rc = re.compile('|'.join(map(re.escape, DictionaryReplace)))
    def translate(match):
        return DictionaryReplace[match.group(0)]
    return rc.sub(translate, text)

def strip_non_ascii(text):
    """ Returns the text without non ASCII characters """
    stripped = (c for c in text if 0 < ord(c) < 127)
    return ''.join(stripped)








