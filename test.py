a0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
print(a0)

a1 = range(10)
print(a1)

a2 = [i for i in a1 if i in a0]
print(a2)

a3 = [a0[s] for s in a0]
print(a3)

a4 = [i for i in a1 if i in a3]
print(a4)

a5 = {i:i*i for i in a1}
print(a5)

a6 = [[i,i*i] for i in a1]
print(a6)



def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
    print(l)

f(2)
f(3,[3,2,1])
f(3)

