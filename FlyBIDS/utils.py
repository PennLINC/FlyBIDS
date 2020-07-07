import re

def get_nested(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return None
    return dct

def extract(string, pattern):

    found = re.search(pattern, string)
    if found:
        return found.group(0)
    else:
        return ''
