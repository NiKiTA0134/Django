my_dict = {
    'fruit': ['apple', 'banana', 'orange'],
    'color': ['red', 'green', 'blue'],
    'animal': ['dog', 'cat', 'rabbit']
}


for value in my_dict.values():
    for i in value():
        print(i)
