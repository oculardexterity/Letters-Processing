import inspect

def myfunc(a, b):
	pass

print(inspect.getargspec(myfunc)[args])