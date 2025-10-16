from distutils.util import run_2to3
from re import L
from uuid import RFC_4122


a=1+5
print (a)

2+3

a=1+2
a=3+4
print(a)

a=2
print(a)
a=a+3
print(a)

pr=1000
dis=15
pr=pr*(100-dis)/100
print(pr)

a=2**100
print(a)

a=1
b=1/2
c="abd"
print(a)
print(b)
print(c)
print(type(a))
print(type(b))
print(type(c))

a=2
b=5
print(id(a), id(b))

# xの平方根を求める
# NG 
# x=2.0
#float rnew, r1, r2
#for(){
 #   rnew = r1
  #  r2 = x / r1
   # rnew = (r1 + r2) / 2
#}

x = 3 
rnew = x
for i in range(10):
    r1 = rnew
    r2 = x/r1
    rnew = (r1 + r2)/2
    print(r1, rnew, r2)

x = 3
rnew = x
for i in range(100000000):
    r1 = rnew
    r2 = x/r1
    rnew = (r1 + r2)/2
print(r1, rnew, r2)


for i in range(10):
    if i == 1:
        continue
    if i ==8:
        break
    print(i)


list(range(10))

list(range(5, 9))

list(range(0, 20, 2))


for i in range(5):
    for j in range(5):
        print(i, j)


for i in range(3):
    for j in range(i):
        print(i, j)


for i in ["田中", "佐藤", "加藤"]:
    for j in ["太郎", "次郎", "三郎"]:
        cross = i + j
        print(cross)


x = 2
rnew = x
diff = rnew - x/rnew
if(diff < 0):
    diff = -diff
while(diff > 10**(-6)):
    r1 = rnew
    r2 = x/r1
    rnew = (r1 + r2)/2
    print(r1, rnew, r2)
    diff = r1 - r2
    if(diff < 0):
        diff = -diff
    if(diff < 10**(-6)):
        break

while True:
    x = input("Input the positive number:")
    try:
        x = float(x)
    except ValueError:
        print(x, " cannot change to number.")
        continue
    except:
        print(" is an unexpected error.")
        exit()
    if(x <= 0):
        print(x, " is not positive number.")
        continue
    #正しい入力が得られた時
    print(x)
    break

    

c = 2.99792458E8
na = 6.02214076E23
form = 'light speed is {0:12.8g} m/s, Avogadro number is {1:12.8g} mol**(-1).'
print(form.format(c,na))




