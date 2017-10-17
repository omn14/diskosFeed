
filUTM = open("oyer_irap_fix.txt",'r')
filLATLON = open("oyer_MESTER.txt",'r')

filOUT = open("out001.txt",'w')
t = 1

for lutm in filUTM:
	#print lutm
	
	if "999.0 999.0 999.0" in lutm:
		print lutm
		t = t + 1
		filOUT.close()
		filOUT = open("out"+str(t).zfill(3)+".txt",'w')
		continue
	filOUT.write(filLATLON.readline())
#	print filLATLON.readline()
	
filUTM.close()
filLATLON.close()
filOUT.close()
