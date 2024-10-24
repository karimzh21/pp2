my_list = ['apple', 'banana', 'cherry']

with open('output.txt', 'w') as file:
    for item in my_list:
        file.write(f"{item}\n")
