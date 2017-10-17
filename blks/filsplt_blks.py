
filUTM = open("blks_fix.txt",'r')
filLATLON = open("blks_latlong.txt",'r')

filOUT = open("blk00001.txt",'w')
t = 1

for lutm in filUTM:
	#print lutm
	
	if "999.0 999.0 999.0" in lutm:
		print lutm
		t = t + 1
		filOUT.close()
		filOUT = open("blk"+str(t).zfill(5)+".txt",'w')
		continue
	filOUT.write(filLATLON.readline())
#	print filLATLON.readline()
	
filUTM.close()
filLATLON.close()
filOUT.close()
