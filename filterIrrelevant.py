#remove values with irrelevant information 
# such as data with only IDs and data with only names

import xml.etree.ElementTree as ET
import datetime
import json

tags = ['bicycle','highway', 'lanes', 'maxspeed', 'oneway']
params = ['service', 'footway', 'steps', 'pedestrian', 'path']


treeroot = ET.Element("root")


#parsing the data file from opensourcemaps
print('parsing...')
print(datetime.datetime.now())

tree = ET.parse('roaddata/filtered/out-brooklyn.xml')

print('done parsing!')
print(datetime.datetime.now())

root = tree.getroot()



print('(XML) removing invalid inputs and IDs')
for road in root.findall('road'):
	if(len(road.getchildren()) < 3):
		root.remove(road)
		continue
	for tag in road:
		if(tag.tag == 'highway'):
			if(params.__contains__(tag.text)):
				root.remove(road)
		if(tag.tag == 'id'):
			road.remove(tag)

print(datetime.datetime.now())


print('creating dictionary')
streetDict = dict()
for road in root.findall('road'):
    key = ""
    values = dict()
    for tag in road:
        if(tag.tag == 'name'):
            key = tag.text
        elif(tag.tag == 'maxspeed'):
        	speed = float(tag.text[0:2]) * 1.60934
        	values[tag.tag] = speed
        else:
            values[tag.tag] = tag.text
    streetDict[key] = values
     

print(datetime.datetime.now())

print('adding missing params and removing unnecessary values')

for key in list(streetDict):
    values = streetDict[key]

    if(len(values)<3):
        del streetDict[key]
        continue
    if(params.__contains__(values['highway'])):
        del streetDict[key]
        continue

    for tag in tags:
        if(tag not in values):
            values[tag] = None
  
print('done filtering!')
json = json.dumps(streetDict)
f = open("filtered-brooklyn.json", "w")
f.write(json)
f.close()







