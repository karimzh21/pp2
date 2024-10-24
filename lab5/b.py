import re

def match_ab2to3(s):
    pattern = r'^ab{2,3}$'
    return bool(re.match(pattern, s))

print(match_ab2to3('abb'))   
print(match_ab2to3('abbb'))  
print(match_ab2to3('abbbb')) 
