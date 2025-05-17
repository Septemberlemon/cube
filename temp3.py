a = {1: 2, 2: 3, 3: 4, 4: 1}
b = {2: 3, 3: 7, 7: 2}
c = {k: a.get(b.get(k, k), b.get(k, k)) for k in set(a) | set(b)}
print(c)
for k in set(a) | set(b):
    print(k)
