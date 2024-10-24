import re

def split_on_uppercase(s):
    return re.findall('[A-Z][^A-Z]*', s)

print(split_on_uppercase('ThisIsAnExample'))

