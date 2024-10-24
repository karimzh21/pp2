import re

def replace_with_colon(s):
    return re.sub(r'[ ,\.]', ':', s)

text = 'Python, Java. C++ Programming Language'
print(replace_with_colon(text))

