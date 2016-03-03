from ctypes import *

class Int():
    _fields_ = [("first_16", c_int, 16), ("second_16", c_int, 16)]

a = Int()
a.first_16 = 20
a.second_16 = 40
print(a.first_16)
