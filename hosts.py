
with open('hosts.txt') as file:
    lines = file.readlines()

print(lines)
for i in range(len(lines)):
    lines[i] = lines[i][8:]
    lines[i] = lines[i][:-1]
    lines[i] = '"*://*.' + lines[i] + '/*",\n'

file2 = open('hosts2.txt', 'w')
for i in lines:
    file2.write(i)
