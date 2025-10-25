import sys

avg = 9
i = 1
k = 3
listB = [1, 2, 3, 4, 5, 6, 7, 7, 7]
listA = [avg] + listB[0:i] + listB[i + k:]
listA.sort()
print(listA)

print(sys.maxsize)
