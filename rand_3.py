import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np                                                               
import matplotlib.pyplot as plt

root = []
dist = ['ariyalur','madurai','theni']#,'coimbatore','cuddalore','dharmapuri','dindigul','erode','kanniyakumari','karur']
for i in dist:
	link = urllib2.urlopen('https://'+i+'.nic.in/')
	source = link.read()
	content = BeautifulSoup(source)

	revenue = content.findAll(('div'),attrs={'class':'list-text blue-color'})
	for i in revenue:
		y = i.text

	rev_content = [int(x) for x in re.findall('\d+',y)]
	sorted_rev_content = sorted(rev_content)
	if len(sorted_rev_content) == 4:
		del sorted_rev_content[2]

	#print sorted_rev_content

	
	general = content.findAll(('div'),attrs = {'class':'vc_column-inner vc_custom_1516774292620'})	
	try:
		for j in general:
			yy = j.text
			zz = yy.replace(',', '')

		gen_content = [float(u) for u in re.findall('\d+\d+\.?\d+',zz)]
		sorted_gen_content = sorted(gen_content)
		if len(sorted_gen_content) == 4:
			del sorted_gen_content[1:3]
		elif len(sorted_gen_content) == 6:
			sorted_gen_content = sorted_gen_content[2:3] + sorted_gen_content[5:]

		#print sorted_gen_content

	except NameError:
		general = content.findAll(('div'),attrs = {'class':'vc_column-inner vc_custom_1537764220850'})
		for j in general:
			yy = j.text
			zz = yy.replace(',', '')


		gen_content = [float(u) for u in re.findall('\d+\d+\.?\d+',zz)]
		sorted_gen_content = sorted(gen_content)
		if len(sorted_gen_content) == 4:
			del sorted_gen_content[1:3]
		elif len(sorted_gen_content) == 6:
			sorted_gen_content = sorted_gen_content[2:3] + sorted_gen_content[5:]

		#print sorted_gen_content

	dist_details = sorted_rev_content + sorted_gen_content
	root.append(dist_details)

print root

content = [(dist[0],root[0][2]),(dist[1],root[1][2]),(dist[2],root[2][2])]


dists = zip(*content)[0]
area = zip(*content)[1]
x_pos = np.arange(len(dists)) 

plt.bar(x_pos,area)
plt.legend()
plt.show()
'''
index = np.arange(len(dist))
plt.bar(dist,)
'''