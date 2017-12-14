import numpy

v = numpy.array ([-1, -7, 20])

a = numpy.array ([1, 3, 4])
b = numpy.array ([20, 40, 60])
c = numpy.array ([100, -120, 30])

M = numpy.array([
    [1, 20, 100],
    [3, 40, -120],
    [4, 60, 30]
])

print (numpy.cross (v, a))
print ()
print (numpy.cross (v, b))
print ()
print (numpy.cross (v, c))
print ()
print ()

print (numpy.cross (v, M, axisb = 0, axisc = 0))
print ()

