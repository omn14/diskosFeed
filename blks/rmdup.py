import sys

if len(sys.argv)<2:
	print "input argument mangler: avslutter ..."
	sys.exit()

print str(sys.argv[1])

filin = open(str(sys.argv[1]),'r')
filout = open(str(sys.argv[1]).split('.')[0]+"_fix.txt",'w')
tmp = "kuk"
for l in filin:
	
	if tmp not in l:
		filout.write(l)
	tmp = l
