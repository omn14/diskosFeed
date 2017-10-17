import numpy as np
c = np.array([])
f = open("sum.html")

for lines in f:
	c = np.append(c,lines)
#	print lines

if c[0]==c[0]:
	print "c0!!!"
if c[0]==c[1]:
	print "c1!!!"

print c[0]
print "\n"
print c[0].split("DATASET ID")[1].split('</a>')[0].split('>')[1]
