from random import randint
a = randint(0,256)
b = randint(0,256)
c = randint(0,256)

for i in range(50):
    print(i)
    if i > 20:
        break

print('ses')

l = [[[2,2],[3,4],[5,6],[7,8]],[1,2,3,4,5,6,7,8]]
avarage = [sum(col) for col in zip(*l[0])]
print('avg ', avarage)
print(len(l[0]))
print(a, b, c)
dist = 2**.5
print(dist)