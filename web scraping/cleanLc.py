
with open('Q_lc.txt', 'r') as f:
    lines = f.readlines()

ans=[]
for i in lines:
    if '/solution' not in i:
        ans.append(i)

with open('lc.txt', 'a') as f:
    for j in ans:
        f.write(j)
