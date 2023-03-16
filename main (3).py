
def accumulate (f1, nulval, nofilter, f, a, next,b, filter):
    if(a>b):
        return nulval
    elif not filter(a):
        return f1(accumulate(f1, nulval, nofilter, f, next(a), next, b, filter ),nofilter)
    else:
        print(a)
        return f1(accumulate(f1, nulval, nofilter, f, next(a), next, b, filter ), f(a))

f= lambda x: 3*x**2-1
a=-10
b=10
dx=0.5
f1= lambda a,b: a+b*dx
filter= lambda x: x<1 or x>-1
next= lambda x: x+dx
print(accumulate(f1, 0, 0, f, a+dx/2, next, b, filter))
