import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np                                                               
import matplotlib.pyplot as plt

list_of_dists = ['madurai','virudhunagar','ramanathapuram','sivaganga','ariyalur','chennai','theni','dindigul','thoothukudi']
root = []

#dist_1 = str(raw_input("Enter The district 1:"))
#dist_2 = str(raw_input("Enter The district 2:"))

#list_of_dists.append(dist_1)
#list_of_dists.append(dist_2)

for i in list_of_dists:
	link = urllib2.urlopen('https://'+i+'.nic.in/')
	source = link.read()
	content = BeautifulSoup(source)

	if i == 'ramanathapuram' or i == 'thanjavur' or i == 'vellore':
		revenue = content.findAll(('div'),attrs={'class':'list-text green-color'})
		for i in revenue:
			y = i.text

	elif i == 'pudukkottai':
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

		#sometimes here if..else ariyalur,theni,krishn,nellai,trichy,tiruvallur,tiruvannmlai,tirupur,tiruvarur	
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

	dist_details = sorted_rev_content + sorted_gen_content
	root.append(dist_details)

print root

divisions = []
taluks = []
villages = []
population = []
i = 0
while i < len(root):
	x = root[i][0]
	divisions.append(x)
	y = root[i][1]
	taluks.append(y)
	z = root[i][2]
	villages.append(z)
	w = root[i][3]
	population.append(w)
	i = i+1
'''
print divisions
print taluks
print villages
print population


print "\n 1 - Divisions\n 2 - Taluks\n 3 - Villages\n 4 - Area\n 5 - Population"

x_axis = zip(*final)[0]
y_axis = zip(*final)[1]
x_pos = np.arange(len(list_of_dists)) 
'''
def plot_graphs(x):
	index = np.arange(len(list_of_dists))
	plt.bar(index,x,align='center')
	plt.xticks(index,list_of_dists,fontsize = 10)
	plt.show()

plot_graphs(population)
