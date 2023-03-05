def f1(x):
 return 3*x*x+1 
 
def func(f, a, b, dx, i=0):
    x=a+i*dx+dx/2
    if(x>b):
        return 0.0
    else:
        return f1(x)*dx +func(f,a, b,dx, i+1)
        


print(func(f1,a=-10,b=10,dx=0.5))