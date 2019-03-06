lis = [0,1,2,4,7,3,2,0]
l = []
print(len(lis))
for i in range(len(lis)-1):
    print(lis[i+1]-lis[i])
    l.append(lis[i+1]-lis[i])
print(l)
print(len(l))

