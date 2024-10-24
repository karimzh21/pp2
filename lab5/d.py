import re

def match_capital_followed_by_lower(s):
    pattern = r'^[A-Z][a-z]+$'
    return bool(re.match(pattern, s))

print(match_capital_followed_by_lower('Python'))  
print(match_capital_followed_by_lower('python'))  
