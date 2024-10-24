import re

def match_a_anything_b(s):
    pattern = r'^a.*b$'
    return bool(re.match(pattern, s))

print(match_a_anything_b('a123b')) 
print(match_a_anything_b('ab'))    
print(match_a_anything_b('a123'))  

