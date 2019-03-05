import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np                                                               
import matplotlib.pyplot as plt
import ogr
import geopandas as gp

list_of_dists = []
root = []

data = ogr.Open("tamil_districts.shp",update = 1)
layer = data.GetLayer()
for i in layer:
	j =  i.GetField("FIRST_DIST")
	list_of_dists.append(j)
    
layer = data.GetLayerByName('tamil_districts')
layer.ResetReading

field_defn = ogr.FieldDefn( "DIVSION", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "TALUK", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "VILLAGE", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "POPULATION", ogr.OFTInteger )
layer.CreateField(field_defn)

#dist_1 = str(raw_input("Enter The district 1:"))
#dist_2 = str(raw_input("Enter The district 2:"))

#list_of_dists.append(dist_1)
#list_of_dists.append(dist_2)


for i in list_of_dists:
    try:
    	link = urllib2.urlopen('https://'+i+'.nic.in/')
    	source = link.read()
    	content = BeautifulSoup(source)
    
    	try:
    		if i == 'ramanathapuram' or i == 'thanjavur' or i == 'vellore':
    			revenue = content.findAll(('div'),attrs={'class':'list-text green-color'})
    			for i in revenue:
    				y = i.text
    
    		elif i == 'pudukkottai' or i == 'kanniyakumari':
    			revenue = content.findAll(('div'),attrs={'class':'list-text red-color'})
    			for i in revenue:
    				y = i.text
    
    		elif i == 'kancheepuram': #kanchi division and taluks get omitted
    			revenue = content.find(('div'),attrs={'class':'list-text blue-color'})
    			for i in revenue:
    				y = i 
    
    		else:	
    			#sometimes here if..else pudukottai,ramnad,tanjore,vellore
    			revenue = content.findAll(('div'),attrs={'class':'list-text blue-color'})
    			for i in revenue:
    				y = i.text
    		
    		rev_content = [int(x) for x in re.findall('\d+',y)]
    		sorted_rev_content = sorted(rev_content)
    		#print sorted_rev_content
    		if len(sorted_rev_content) == 4:
    			del sorted_rev_content[2]
    		if len(sorted_rev_content) == 1:
    			sorted_rev_content = [0,0] + sorted_rev_content
    
    	except NameError:
    		sorted_rev_content = [0,0,0]		
    			
    	try:	#sometimes here if..else ariyalur,theni,krishn,nellai,trichy,tiruvallur,tiruvannmlai,tirupur,tiruvarur	
    		general = content.findAll(('div'),attrs = {'class':'wpb_column vc_column_container vc_col-sm-4 vc_col-has-fill'})
    		for j in general:
    			yy = j.text
    			zz = yy.replace(',', '')
    
    		gen_content = [float(u) for u in re.findall('\d+\d+\.?\d+',zz)]
    		sorted_gen_content = sorted(gen_content)
    		#print sorted_gen_content
    		if len(sorted_gen_content) == 0:
    			sorted_gen_content = [0] #tiruvannamalai area gets omitted
    		n = len(sorted_gen_content)
    		sorted_gen_content = sorted_gen_content[n-1:]
    
    	except NameError:
    		sorted_gen_content = [0]	
    		
    	dist_details = sorted_rev_content + sorted_gen_content
    	root.append(dist_details)
    
    except:
        dist_details = [0,0,0,0]
        root.append(dist_details)

#print root

data = ogr.Open("tamil_districts.shp",update = 1)
layer = data.GetLayer()
j = 0
for i in layer:
    i.SetField('DIVSION',root[j][0])
    layer.SetFeature(i)
    i.SetField('TALUK',root[j][1])
    layer.SetFeature(i)
    i.SetField('VILLAGE',root[j][2])
    layer.SetFeature(i)
    i.SetField('POPULATION',root[j][3])
    layer.SetFeature(i)
    j = j+1
data = None

divisions = []
taluks = []
villages = []
population = []
i = 0
for i in range(len(root)):
	x = root[i][0]
	divisions.append(x)
	y = root[i][1]
	taluks.append(y)
	z = root[i][2]
	villages.append(z)
	w = root[i][3]
	population.append(w)

def plot_graphs(x):
	index = np.arange(len(list_of_dists))
	plt.bar(index,x,align='center')
	plt.xticks(index,list_of_dists,fontsize = 10,rotation = 90)
	plt.show()

plt.figure(1,figsize=(12,8))
plt.subplot2grid((2,2), (0,0))
plt.title('DIST WISE POPULATION')
plot_graphs(population)

plt.subplot2grid((2,2), (0,1))
plt.title('VILLAGES IN TN')
plot_graphs(villages)

map_content = gp.read_file('tamil_districts.shp')

plt.subplot2grid((2,2), (1,0))
plt.title('DIST WISE POPULATION')
map_content.plot('POPULATION',cmap='YlGn')

plt.subplot2grid((2,2), (1,1))
plt.title('VILLAGES IN TN')
map_content.plot('VILLAGE',cmap='YlGnBu')

plt.show()


