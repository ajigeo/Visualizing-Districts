import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np                                                               
import matplotlib.pyplot as plt
import ogr
import geopandas as gp

list_of_dists = [] #list containing all the district names taken from the shapefile
root = [] #list of list with the sdistrict name and the 4 attributes - divion, taluk,village,population

#open the shapefile and gets the district name alone from FIRST_DIST column
data = ogr.Open("tamil_districts.shp",update = 1)
layer = data.GetLayer()
for i in layer:
	j =  i.GetField("FIRST_DIST")
	list_of_dists.append(j)
    
layer = data.GetLayerByName('tamil_districts')
layer.ResetReading
#creates the 4 columns which we want 
field_defn = ogr.FieldDefn( "DIVSION", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "TALUK", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "VILLAGE", ogr.OFTInteger )
layer.CreateField(field_defn)
field_defn = ogr.FieldDefn( "POPULATION", ogr.OFTInteger )
layer.CreateField(field_defn)

#iterate through all the districts and get the data
for i in list_of_dists:
    try:
    	link = urllib2.urlopen('https://'+i+'.nic.in/')
    	source = link.read()
    	content = BeautifulSoup(source)
    
    	try: #revenue contents in green color 
    		if i == 'ramanathapuram' or i == 'thanjavur' or i == 'vellore':
    			revenue = content.findAll(('div'),attrs={'class':'list-text green-color'})
    			for i in revenue:
    				y = i.text
    
    		elif i == 'pudukkottai' or i == 'kanniyakumari': #revenue contents in pink color
    			revenue = content.findAll(('div'),attrs={'class':'list-text red-color'})
    			for i in revenue:
    				y = i.text
    
    		elif i == 'kancheepuram': #kanchi has many contents in blue color so used only find instead of findall
    			revenue = content.find(('div'),attrs={'class':'list-text blue-color'})
    			for i in revenue:
    				y = i 
    
    		else:	
    			#works for most of the districts in this way
    			revenue = content.findAll(('div'),attrs={'class':'list-text blue-color'})
    			for i in revenue:
    				y = i.text
    		
    		rev_content = [int(x) for x in re.findall('\d+',y)]
    		sorted_rev_content = sorted(rev_content)
    		#print sorted_rev_content and limit the length of contents to 3
    		if len(sorted_rev_content) == 4: 
    			del sorted_rev_content[2]
    		if len(sorted_rev_content) == 1:
    			sorted_rev_content = [0,0] + sorted_rev_content
    
    	except NameError: #for vellore
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
    
    except: #for nagapattinam
        dist_details = [0,0,0,0]
        root.append(dist_details)

#open the shape file and add the contents districtwise from root
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

#from root take all the attributes and store it in lists for bar plot
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

#bar plot
fig = plt.figure()
fig.set_size_inches(15,15)
fig.suptitle('POPULATION')
index = np.arange(len(list_of_dists))
plt.bar(index,population,align='center')
plt.xticks(index,list_of_dists,fontsize = 10,rotation = 90)
fig.savefig('POP_BAR.png')

fig = plt.figure()
fig.set_size_inches(15,15)
fig.suptitle('VILLAGES')
index = np.arange(len(list_of_dists))
plt.bar(index,villages,align='center')
plt.xticks(index,list_of_dists,fontsize = 10,rotation = 90)
fig.savefig('VILLAGE_BAR.png')

#choropleth map using gpd
map_content = gp.read_file('tamil_districts.shp')

map_content.plot('POPULATION',cmap='YlGn')
plt.savefig('POP_COR.png',dpi=1080)


map_content.plot('VILLAGE',cmap='YlGnBu')
plt.savefig('VILLAGE_COR.png',dpi=1080)

