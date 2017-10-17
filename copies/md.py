import feedparser
import urllib2
import numpy as np
import math

#import pandas as pd
from adjustText import adjust_text


import matplotlib.pyplot as plt, mpld3
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
#import matplotlib.patches as patches
def loadCoast(t):
	return np.genfromtxt(t,usecols=(0,1))

def loadFlds(t):
	f = open(t,'r')
	t=0;
	print "laster felt"
	navn = np.array([])
	lat = np.array([])
	lon = np.array([])
	for l in f:
		if t==0:
			t = t + 1
			continue
		#print l
		
		navn = np.append(navn,l.split(',')[1])
		k = l.replace("MULTIPOLYGON(((","POLYGON((")
		nums = str(k.split("POLYGON((")[1]).split(",")
		#print nums
		for n in nums:
			#print n
			ll = str(n.split(" ")[1]).replace(')','')
			ll = ll.replace('\n','')
			ll = ll.replace('\r','')
			ll = ll.replace('"','')
			ll = ll.replace('(','')
			lo = str(n.split(" ")[0]).replace(')','')
                        lo = lo.replace('\n','')
                        lo = lo.replace('\r','')
                        lo = lo.replace('"','')
			lo = lo.replace('(','')
			lat = np.append(lat,float(ll))
			lon = np.append(lon,float(lo))
		lat = np.append(lat,float(-999))
                lon = np.append(lon,float(-999))
#		lat = np.append(lat,str(str(k.split("POLYGON((")[1]).split(",")).split(" ")[1])
#		lon = np.append(lon,str(str(k.split("POLYGON((")[1]).split(",")).split(" ")[0])
#		print lat
		t = t + 1
	return navn, np.column_stack((lat,lon))

def ll2rad(d,m,s):
	deg = float(d) + (float(m)/60.0) + (float(s)/60.0/60.0)
	rad = (deg * math.pi) / 180
	return rad

print "import ok"

'''
% LLA2ECEF - convert latitude, longitude, and altitude to
%            earth-centered, earth-fixed (ECEF) cartesian
% 
% USAGE:
% [x,y,z] = lla2ecef(lat,lon,alt)
% 
% x = ECEF X-coordinate (m)
% y = ECEF Y-coordinate (m)
% z = ECEF Z-coordinate (m)
% lat = geodetic latitude (radians)
% lon = longitude (radians)
% alt = height above WGS84 ellipsoid (m)
% 
% Notes: This function assumes the WGS84 model.
%        Latitude is customary geodetic (not geocentric).
% 
% Source: "Department of Defense World Geodetic System 1984"
%         Page 4-4
%         National Imagery and Mapping Agency
%         Last updated June, 2004
%         NIMA TR8350.2
% 
% Michael Kleder, July 2005
'''
def lla2ecef(lat,lon,alt):

	# WGS84 ellipsoid constants:
	a = 6378137;
	e = 8.1819190842622e-2;

	# intermediate calculation
	# (prime vertical radius of curvature)
	N = a / math.sqrt(1 - e**2 * math.sin(lat)**2);

	# results:
	x = (N+alt) * math.cos(lat) * math.cos(lon);
	y = (N+alt) * math.cos(lat) * math.sin(lon);
	z = ((1-e**2) * N + alt) * math.sin(lat);

	return x,y,z

def loadCoast2(t):
        fil = open(t)
        lat = np.array([])
        lon = np.array([])
        latc = 0
        lonc = 0
        for lines in fil:
		l1 = lines[0:10]
		l2 = lines[30:40]
		print l1
		print l2
                #latc = (float(lines[0:10])*math.pi)/180
		#lonc = (float(lines[30:40])*math.pi)/180
		latc = (float(l1)*math.pi)/180
		latc,lonc,z = lla2ecef(latc,lonc,0)
		lat = np.append(lat,latc)
                lon = np.append(lon,lonc)

        return np.column_stack((lat,lon))

def getcoords(surv):
	print surv.encode('utf-8')
	pol = open("surveyCoordinatesIncTurnarea.csv",'r')
	lat = np.array([])
	lon = np.array([])
	for line in pol:
      		if (line.split(',')[0] == surv.encode('utf-8')):
		#	print line
			print line #.decode('utf-8')
			l = line.split(',')
			lat = np.append(lat,ll2rad(l[3],l[4],l[5]))
			lon = np.append(lon,ll2rad(l[6],l[7],l[8]))


	pol.close()
	return lat,lon


def readDB(fn):
	c = np.array([])
	cn = np.array([])
	f = open(fn)
	
	for lines in f:
	        c = np.append(c,lines)
		cn = np.append(cn,lines.split("DATASET ID")[1].split('</a>')[0].split('>')[1])
	#       print lines
	
	if c[0]==c[0]:
	        print "c0!!!"
	if c[0]==c[1]:
        	print "c1!!!"

	print c[0]
	print "\n"
	print cn[0]	
	
	return c,cn

def compare(a,b):
	for i in a:
#		print i
		if i==b:
			print "found match entry nr. ", b
			return True
	print "NO match entry nr. ", b
	return False

def extract(ar,s):
	a = np.array([])
	for l in ar:
		a = np.append(a,l.split(s)[1].split('</a>')[0].split('>')[1])
	return a

auth = urllib2.HTTPBasicAuthHandler()
auth.add_password("Spring Security Application", 'https://member.diskos.cgg.com/whereoil-data/feed/mydks/', "o.eiesland@searchergeo.com", 'Krabbe2405')



'''
d = feedparser.parse('https://member.diskos.cgg.com/whereoil-data/feed/mydks/mydks:MyDatasets.atom?\
kadme.security.token=4d7a454e59546b7a595463314f6a4e745953306a4c6a6c305957456b4e324d77594451744f7a4a\
344e44416a346d4d78&q=base64:eyJxdWVyeSI6eyJjbGFzc25hbWUiOiJteWRrczpNeURhdGFzZXRzIiwiYW5kIjpbeyJhbmQ\
iOlt7Imxpa2UiOlt7Im15ZGtzOkVOVF9TVEFUVVMiOiIqWUVTKiJ9XX1dfV19LCJzdGFydCI6MCwiY291bnQiOjEwMCwgInBhZ2\
luYXRpb24iOnsic29ydHMiOlt7InNvcnQiOiAia21ldGE6TGFzdE1vZGlmaWVkIiwiZGlyIjoiREVTQyJ9XX19',handlers=[auth])
'''

d = feedparser.parse('https://o.eiesland@searchergeo.com:Krabbe2405@\
member.diskos.cgg.com/whereoil-data/feed/mydks/mydks:MyDatasets.atom?\
kadme.security.token=4d7a454e59546b7a595463314f6a4e745953306a4c6a6c305957456b4e324d77594451744f7a4a\
344e44416a346d4d78&q=base64:eyJxdWVyeSI6eyJjbGFzc25hbWUiOiJteWRrczpNeURhdGFzZXRzIiwiYW5kIjpbeyJhbmQ\
iOlt7Imxpa2UiOlt7Im15ZGtzOkVOVF9TVEFUVVMiOiIqWUVTKiJ9XX1dfV19LCJzdGFydCI6MCwiY291bnQiOjEwMCwgInBhZ2\
luYXRpb24iOnsic29ydHMiOlt7InNvcnQiOiAia21ldGE6TGFzdE1vZGlmaWVkIiwiZGlyIjoiREVTQyJ9XX19')



print d
print " "

print d.status
'''
print " "
print d.headers
print " "
'''
print d.entries[0]['updated']
print d.entries[0]['updated_parsed']
print d.entries[0]['links']
#print d.entries[0]['type']
#print d.entries[0]['rel']
print d.entries[0]['title']
print d.entries[0]['author']
print d.entries[0]['summary']
print d.entries[0]['content']
print len(d.entries[0])
print len(d.entries)

'''
f = open("sum.html",'w')
k=str(d.entries[0]['summary'])
f.write(k+'\n')
f.write(str(d.entries[1]['summary'])+'\n')
f.close()
'''

e=np.array([])
for i in range(len(d.entries)):
	e = np.append(e,d.entries[i]['summary'])

for i in d:
	print i

cf, cfn = readDB("sum.html")

print cf[0]
print cfn[0]

f = open("sum.html",'a')
xx=0
for x in extract(e,"DATASET ID"):
	if (not compare(extract(cf,"DATASET ID"),x)):
		print "Updating Database"
		f.write(str(d.entries[xx]['summary'])+'\n')

	xx=xx+1
f.close()
		

#print compare(extract(cf,"DATASET ID"),extract(e,"DATASET ID"))


#print cf[0]
#print e[0]
#print str(cf[0]) == str(e[0])

fig, ax = plt.subplots()
patches = []
#find coords:----------------------------------------------
surveys = extract(e,"SURVEY NAME")
print surveys

texts = []

for ss in np.array([0,8,10,18,29]):
#**********************************************************
	latc,lonc = getcoords(surveys[ss])
	print latc
	print lonc

	print "lengde ---", len(latc)
	for i in range(len(latc)):
		latc[i],lonc[i],zzz= lla2ecef(latc[i],lonc[i],0)

	print latc
	print lonc

	coord = np.column_stack((latc,lonc))
	#coord = 0.0000001*coord
	print coord
	print np.shape(coord)

	tmp2 = np.copy(-coord[:,0])
	coord[:,0]=coord[:,1]
	coord[:,1]=tmp2
	print coord
	#a = np.array([[1,2,3],[4,3,1]])
	ii = coord[:,1].argmax()
	#a[i,j]
	
	#ax.annotate(surveys[ss], xy=(coord[ii,0],np.max(coord[:,1])), 
	#	    xytext=(coord[ii,0]-10000,np.min(coord[:,1])+250000),
	#	    arrowprops=dict(facecolor='grey', shrink=0.05))
	
	texts.append(ax.text(coord[ii,0],np.max(coord[:,1]),surveys[ss]))
	
	polygon = Polygon(coord, True)
	patches.append(polygon)

#----------------------------------------------------------

#adjust_text(texts, force_text=0.05, arrowprops=dict(arrowstyle="-|>",
#                                                    color='r', alpha=0.5))

for i in range(1,10): 
#**********************************************************
	kyst = loadCoast("0"+str(i)+"spltNCL.txt")


	print kyst[0]

	kyst = (kyst * math.pi)/180.0
	for i in range(len(kyst[:,0])):
		kyst[:,0][i],kyst[:,1][i],zzz= lla2ecef(kyst[:,0][i],kyst[:,1][i],0)

	tmp = np.copy(-kyst[:,0])
	kyst[:,0]=kyst[:,1]
	kyst[:,1]=tmp

	polygon = Polygon(kyst, True)
	patches.append(polygon)
#----------------------------------------------------------
for i in range(1,4):
#**********************************************************
	kyst = loadCoast("0"+str(i)+"splitAPA.txt")


	print kyst[0]

	kyst = (kyst * math.pi)/180.0
	for i in range(len(kyst[:,0])):
		kyst[:,0][i],kyst[:,1][i],zzz= lla2ecef(kyst[:,0][i],kyst[:,1][i],0)

	tmp = np.copy(-kyst[:,0])
	kyst[:,0]=kyst[:,1]
	kyst[:,1]=tmp

	polygon = Polygon(kyst, True)
	patches.append(polygon)
#----------------------------------------------------------
for i in range(1,365):
#**********************************************************
        kyst = loadCoast("/mnt/c/Users/Ole/Desktop/oyer/out"+str(i).zfill(3)+".txt")


        #print kyst[0]

        kyst = (kyst * math.pi)/180.0
        for i in range(len(kyst[:,0])):
                kyst[:,0][i],kyst[:,1][i],zzz= lla2ecef(kyst[:,0][i],kyst[:,1][i],0)

        tmp = np.copy(-kyst[:,0])
        kyst[:,0]=kyst[:,1]
        kyst[:,1]=tmp

        polygon = Polygon(kyst, True)
        patches.append(polygon)
#----------------------------------------------------------
patches_blks = []
for i in range(1,1828):
#**********************************************************
        kyst = loadCoast("/mnt/c/Users/Ole/Desktop/oyer/blks/blk"+str(i).zfill(5)+".txt")


        #print kyst[0]

        kyst = (kyst * math.pi)/180.0
        for i in range(len(kyst[:,0])):
                kyst[:,0][i],kyst[:,1][i],zzz= lla2ecef(kyst[:,0][i],kyst[:,1][i],0)

        tmp = np.copy(-kyst[:,0])
        kyst[:,0]=kyst[:,1]
        kyst[:,1]=tmp

        polygon = Polygon(kyst, True)
        patches_blks.append(polygon)
#----------------------------------------------------------

#flds, flds_coord = loadFlds("/mnt/c/Users/Ole/Desktop/oyer/flds/fldArea.csv")
#print flds

for i in range(1,2):
#**********************************************************
        #kyst = loadCoast("/mnt/c/Users/Ole/Desktop/oyer/blks/blk"+str(i).zfill(5)+".txt")
	flds, kyst = loadFlds("/mnt/c/Users/Ole/Desktop/oyer/flds/fldArea.csv")

        #print kyst[0]
	kll = np.array([])
	klo = np.array([])
	kyst2 = np.array([])
	for ns in range(len(kyst[:,0])):
		if kyst[ns,0] != -999:
			kll = np.append(kll,kyst[ns,0])
			klo = np.append(klo,kyst[ns,1])
			continue
		kyst2 = np.column_stack((kll,klo))
		kyst2 = (kyst2 * math.pi)/180.0
		for i in range(len(kyst2[:,0])):
			kyst2[:,0][i],kyst2[:,1][i],zzz= lla2ecef(kyst2[:,0][i],kyst2[:,1][i],0)

		tmp = np.copy(-kyst2[:,0])
		kyst2[:,0]=kyst2[:,1]
		kyst2[:,1]=tmp

		polygon = Polygon(kyst2, True)
		patches_blks.append(polygon)
		kyst2 = np.array([])
		kll = np.array([])
		klo = np.array([])
#----------------------------------------------------------
'''
#--
p_blks = PatchCollection(patches_blks,alpha=0.2)
p_blks.set_facecolors('none')#(1, 1, 0, 0.0))
p_blks.set_edgecolors((0, 0, 0, 1.0))
ax.add_collection(p_blks)
#--
'''
for p in patches:
	ax.add_patch(p)

'''
colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, alpha=0.4)
p.set_array(np.array(colors))
p.set_edgecolors((0, 0, 0, 1.0))
ax.add_collection(p)
'''

#fig.colorbar(p, ax=ax)

ax.axis('auto')
adjust_text(texts, force_text=0.5, arrowprops=dict(arrowstyle="->",
                                                    color='black', alpha=0.8))
#print type(coord)
#print type(coord[0])
#print type(coord[0][0])

htmlfil = open("plt.html",'w')
htmlfil.write(mpld3.fig_to_html(fig))
htmlfil.close()
plt.show()
