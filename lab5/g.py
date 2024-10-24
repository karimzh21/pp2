def snake_to_camel(s):
    components = s.split('_')
    return components[0] + ''.join(word.title() for word in components[1:])

print(snake_to_camel('hello_world_example'))

