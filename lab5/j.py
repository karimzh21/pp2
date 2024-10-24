import re

def camel_to_snake(s):
    s = re.sub('([A-Z])', r'_\1', s)
    return s.lower().lstrip('_')

print(camel_to_snake('thisIsAnExample'))
