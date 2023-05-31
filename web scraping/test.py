lines = []
with open('lc.txt', 'r') as file:
    for line in file:
        lines.append(line.strip())
print("length of list",len(lines));    
print(lines[338])