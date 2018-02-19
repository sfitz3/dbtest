import datetime
m=1
j = datetime.date(2011,1,1)
k = j + datetime.timedelta(weeks=1)
print(j, k)
while m < 52:

    j=k+datetime.timedelta(days=1)
    k = j + datetime.timedelta(days=7)
    print(j,k)
    m = m+1

b= datetime.date(2011,3,15)

print ('b is: '+str(b))
s=b.timetuple().tm_year
t=b.timetuple().tm_mon
print(str(s))
print(str(t))
n=0
while n < 365:
    b=b+datetime.timedelta(days=1)
    n=n+1
    print(b)