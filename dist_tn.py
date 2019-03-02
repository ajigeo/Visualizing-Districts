#ariyalur,kanniyakumari,krishnagiri,pudukottai,
#ramnad,theni,tanjore,trichy,tirupur,nellai,tiruvallur,
#tiruvannamali,tiruvarur,vellore districts wont work
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np                                                               
import matplotlib.pyplot as plt

list_of_dists = []
root = []

dist_1 = str(raw_input("Enter The district 1:"))
dist_2 = str(raw_input("Enter The district 2:"))

list_of_dists.append(dist_1)
list_of_dists.append(dist_2)

for i in list_of_dists:
	link = urllib2.urlopen('https://'+i+'.nic.in/')
	source = link.read()
	content = BeautifulSoup(source)

	#sometimes here if..else pudukottai,ramnad,tanjore,vellore
	revenue = content.findAll(('div'),attrs={'class':'list-text blue-color'})
	for i in revenue:
		y = i.text

	rev_content = [int(x) for x in re.findall('\d+',y)]
	sorted_rev_content = sorted(rev_content)
	if len(sorted_rev_content) == 4:
		del sorted_rev_content[2]

	#sometimes here if..else ariyalur,theni,krishn,nellai,trichy,tiruvallur,tiruvannmlai,tirupur,tiruvarur	
	general = content.findAll(('div'),attrs = {'class':'vc_column-inner vc_custom_1516774292620'})
	for j in general:
			yy = j.text
			zz = yy.replace(',', '')

	gen_content = [float(u) for u in re.findall('\d+\d+\.?\d+',zz)]
	sorted_gen_content = sorted(gen_content)
	if len(sorted_gen_content) == 4:
		del sorted_gen_content[1:3]
	elif len(sorted_gen_content) == 5:
		sorted_gen_content = sorted_gen_content[1:2] + sorted_gen_content[4:]
	elif len(sorted_gen_content) == 6:
		sorted_gen_content = sorted_gen_content[2:3] + sorted_gen_content[5:]
	elif len(sorted_gen_content) == 7:
		sorted_gen_content = sorted_gen_content[1:2] + sorted_gen_content[6:]
	elif len(sorted_gen_content) == 8:
		sorted_gen_content = sorted_gen_content[2:3] + sorted_gen_content[7:]

	dist_details = sorted_rev_content + sorted_gen_content
	root.append(dist_details)

print root

print "\n 1 - Divisions\n 2 - Taluks\n 3 - Villages\n 4 - Area\n 5 - Population"

ss = int(raw_input("enter what to plot:"))

final = [(list_of_dists[0],root[0][ss-1]),(list_of_dists[1],root[1][ss-1])]

x_axis = zip(*final)[0]
y_axis = zip(*final)[1]
x_pos = np.arange(len(list_of_dists)) 

plt.bar(x_pos,y_axis)
plt.show()

