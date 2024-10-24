import re

def insert_spaces(s):
    return re.sub(r'(?<!^)([A-Z])', r' \1', s)

print(insert_spaces('ThisIsAnExample'))
