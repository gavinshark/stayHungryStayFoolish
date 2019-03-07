from ctypes import cdll
lib = cdll.LoadLibrary("../VCLib/x64/Release/VCLib.dll")

# C style fucntion call
def c_call():
    print('add(2,3):', lib.add(2, 3))

# class style function call
class Foo(object):
    def __init__(self):
        self.obj = lib.CFoo_new()
    def multiply(self,  a,  b):
        return lib.CFoo_multiply(self.obj, a, b)
    def __del__(self):
        lib.CFoo_delele(self.obj)

def class_call():		
    f = Foo()
    result = f.multiply(2, 3)
    print ('multipy(2,3):', result)
    #del f
    
if __name__ == '__main__':
    c_call()
    class_call()
    #cnt = 0
    #while cnt < 3:
    #    cnt = cnt + 1
    #    class_call()