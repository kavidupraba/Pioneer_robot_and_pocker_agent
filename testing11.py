le=[25,25,25,25]
print(list(set(le)))
lo=[15,16,17,30]
print(list(set(lo)))
r=lambda c,d:c+d
print(r(3,5))

def n (func):
    def f (*arg,**kwargs):
        result=func(arg,kwargs)
        return result
    return f
func