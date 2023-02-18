def first(a):
  return  a*a
  
def second(b):
  return  b*b
  

def f3(f1, f2):
    return lambda x,y: f1(x) + f2(y)
    
fun= f3(first, second)
print(fun(5,6))