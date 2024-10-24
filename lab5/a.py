import re

def match_ab(s):
    pattern = r'^ab*$'
    return bool(re.match(pattern, s))

print(match_ab('a'))     
print(match_ab('abbb'))  
print(match_ab('ac'))    
