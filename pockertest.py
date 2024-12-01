le={"lo":[1,2],"jo":[3,4]}
if le["lo"]:
    print("y")
else:
    print("n")
print(len(set(le["lo"]+le["jo"])))
al=(le["lo"]+le["jo"])
print(al)

a=[1,2,3]
b=[1,2]
n="ka"
t="kal"
if all(i in a for i in b):
    print("y")
else:
    print("n")

if a.__contains__(b):
    print("y")
else:
    print("n")
z=[i in a for i in b]
print(z)