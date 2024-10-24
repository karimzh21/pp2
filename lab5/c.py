import re

def match_lowercase_sequence(s):
    pattern = r'^[a-z]+_[a-z]+$'
    return bool(re.match(pattern, s))

print(match_lowercase_sequence('hello_world')) 
print(match_lowercase_sequence('Hello_world')) 
