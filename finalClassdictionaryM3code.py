# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 00:14:39 2022

@author: sincl
"""
# Final Dictionary Creation Code:
    # Time formating:
        # 8am = 0, 8:30am = 1, 9am = 2 ..... 11pm = 28, 11:30pm = 29
        # M = 0 + T_val, T = 30 + T_val, ... F = 120 + T_val
        # M: [0-29], T: [30-59], W: [60-89], R: [90-119], F: [120-150]
        # Class length = number of half-hours; 2.5 hour class = 5
        # Original l (Raw): [[[[3, 3], [63, 3]], '1-390']] = 
        # = [[[start1, length1], [start2, length2], [start3, length3], [start4, length4], loc]]
        # final time list from all_slots
    # create time range [] key
    # Separate loc from 'l' list; truncate to first digit --> building number (var bldg)
    # Avoid duplicate counting of courses that are the same as each other
    # FINAL DICTIONARY FORMAT
        # {number:1.00, times: [[start1, length1], [start2, length2], ... , [startN, lengthN]], bldg, course}
    # Print to .csv
    
    
import csv
import M3_DataCleaner_FINAL
import json
from collections import OrderedDict

Fjson = M3_DataCleaner_FINAL.finaljson

 
# deleting irrelevant keys (keys not in desired_keys)
desired_keys = ['no', 'co', 'l', 's', 'r', 'b', 'le', 'sa', 't', 'si']
for entry in Fjson:
    delete = [key for key in entry if key not in desired_keys]
    for key in delete: del entry[key]
    

# Adding bldg location key to dictionary "bldg" after condensing "loc" key
for item in Fjson:
    if item['l'] != []:
        item['loc'] = item['l'][0][-1]
    else:
        item['loc'] = "FILL"
        
for item in Fjson:
    if item['loc'] != "FILL":
        splitter = item['loc'].split("-")
        item["bldg"] = splitter[0]
    else:
        item["bldg"] = "N/A"

# for entry in Fjson:
#     if entry['co'] == '15':
#         print(entry)
        
# re-creating l_slots from 'l # RECITATIONS ARE DISREGARDED, b_slots (maybe) considered later
for item in Fjson:
    if item['l'] == []:
        item['l_slots'] = []
    else:
        item['l_slots'] = []
        if len(item['l']) == 1:
            for slot in item['l'][0][:-1][0]:
                item['l_slots'].append(slot)
        if len(item['l']) == 2:
            for listy in item['l']:
                for slot in listy[:-1][0]:
                    item['l_slots'].append(slot)                    
        #assumes that each lecture section is in the same building (rarely false)


        
# avoiding double counting of 'same-as' classes
# make 'same-as' field a list of courses
for item in Fjson:
    if item['sa'] == '':
        item['sa'] = []
    else:
        if ", " in item['sa']:
            item['sa'] = item['sa'].split(", ")
        else: 
            item['sa'] = [item['sa']]
        
# if any 'no' is in another item's 'sa' list, then make average enrollment 'si' = 0,
for item1 in Fjson:
    for item2 in Fjson:
        if item2['no'] in item1['sa'] and item1['si'] != 0.0:
            item2['si'] = 0.0
            


# Adding lat & long keys to the dictionary from MITBuildingLocations CSV
locfile = open('MITBuildingLocations.csv')
csvreader = csv.reader(locfile)
header = next(csvreader)
locationList = []
for row in csvreader:
    locationList.append(row)
for item in Fjson:
    for loc in locationList:
        if item['bldg'] == loc[0]:
            item['lat'] = loc[1]
            item['lon'] = loc[2]
locfile.close()
            

#re-configuring all_slots key: [[[122, 4]], [[3, 3]]] --> [[[122, 126], [3, 6]]]
for item in Fjson:
    if item['l_slots'] == []:
        item['start_end'] = [0, 0] #out of range of possible class times
    else:
        item['start_end'] = [] #initiate list
        for slot in item['l_slots']:
            item['start_end'].append([slot[0], slot[0] + slot[1]])
   

# Dropping unnecessary keys: 'l', 'r', 'b', 'sa', 's', 'loc'
droplist = ['l', 'r', 'b', 'sa', 's', 'loc']
for item in Fjson:
    [item.pop(key) for key in droplist]


##########################################
# Final Data File 
# Creating mapdata list variable --> csv 

# Summing 'si' values for classes in the same bldg (same lat, lon)
mapdata = []
locfile = open('MITBuildingLocations.csv')
csvreader = csv.reader(locfile)
header = next(csvreader)
for row in csvreader:
    mapdata.append([row[0], row[1], row[2], 0]) #current format: [bldg, lat, lon, student count]
    
# Test case: time = 64 , term = 'SP'; 'show' key determines whether class is in session
time = 64
current_term = 'SP'
for item in Fjson:
    if current_term in item['t']:
        if type(item['start_end'][0]) == int:
            if time in range(item['start_end'][0], item['start_end'][1]):
                item['show'] = True
            else:
                item['show'] = False
        else:
            for slot in item['start_end']:
                if time in range(slot[0], slot[1]):
                    item['show'] = True
                else:
                    item['show'] = False
    else:
        item['show'] = False
            
# inputing lat, lon of each building into mapdata list
for item in Fjson:
    if item['show'] == True: #if the class is in session
        for row in mapdata:
            if item['bldg'] == row[0]:
                row[1] = item['lat']
                row[2] = item['lon']
                row[3] += int(item['si'])
                #buildings with 0 student count do not hold any lectures during the given term & time



#################################################
# CREATING GEOJSON CODE:
# Format:
# {
#   {
#   "type": "Feature",
#   "geometry": {
#     "type": "Point",
#     "coordinates": [40, -70]
#   },
#   "properties": {
#     "bldg" : 3  
#     "stud_ct": 20
#   }
# }, ..... }

# mapdata to csv file first
fields = ['bldg', 'lat', 'lon', 'stud_ct']
# with open('mapdata.csv', 'w') as f:
#     write = csv.writer(f) 
#     write.writerow(fields)
#     write.writerows(mapdata)

# mapdata.csv to GeoJson file (for mapbox compatability)
li = []
with open('mapdata.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for bldg, lat, lon, stud_ct in reader:
        d = OrderedDict()
        d['type'] = 'Feature'
        d['geometry'] = {
            'type': 'Point',
            'coordinates': [float(lon), float(lat)]
        }
        d['properties'] = {
            'bldg': bldg,
            'stud_ct': float(stud_ct)
        }
        
        li.append(d)

d = OrderedDict()
d['type'] = 'FeatureCollection'
d['features'] = li
with open('M3mapdata.json', 'w') as f:
    f.write(json.dumps(d, sort_keys=False, indent=4))
    
print("-------------")
print(Fjson[0])
print("-------------")
print(Fjson[1])
print("-------------")
print(Fjson[2])
# print("-------------")
# print(Fjson[3])
# print("-------------")
# print(Fjson[4])
# print("-------------")
# print(Fjson[5])

# for item in Fjson:
#     if item['no'] == '2.017':
#         print(item)
#     if item['no'] == '2.00C':
#         print(item)
#     if item['no'] == 'EC.746':
#         print(item)



