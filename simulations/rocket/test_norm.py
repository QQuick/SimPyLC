import numpy
import math

l = [1, 2, 3]
v = numpy.array (l)

print (numpy.linalg.norm (v))
print (math.sqrt (sum ([x * x for x in l])))

