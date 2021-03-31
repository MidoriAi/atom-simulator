symbols = {}
with open('ex.txt') as file:
    output = []
    file = file.readlines()
    for lines in file:
        output.append(lines.split('\n '))

    for i, elem in enumerate(output):
        symbols[i] = (elem[0].replace('\n', '').split(' - '))
    print(symbols)