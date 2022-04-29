# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 17:12:28 2022

@author: sincl
"""
# full json --> full CSV --> remove header of class keys --> txt file -->
# convert to string --> replace ' with " --> json list --> csv
import json
import csv
import pandas as pd
import re
from ast import literal_eval

#json file to csv
with open('full.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('fullcsv.csv', encoding='utf-8', index=False)


# manually edited fullcsv.csv --> rawrow.csv by deleting header row and transposing data


# rawrow.csv --> rawrowtext.txt text file
with open('rawrowtext.txt', "w") as myOutput:
    with open('rawrow.csv', "r") as myInput:
        [ myOutput.write(" ".join(row)+'\n') for row in csv.reader(myInput)]
    myOutput.close()

# text file to string
text_file = open("rawrowtext.txt", "r")
rawdata = text_file.read()
text_file.close()


# replace ' with " for jason formating
smoothjson = rawdata.replace("\'", "\"")
smoothlist = rawdata.splitlines()

# create list of dictionaries from each item of smoothlist
finaljson = []
for row in smoothlist:
    entry = eval(row)
    finaljson.append(entry)

#list of dictionary keys
class_info = ['no', 'co', 'cl', 'tb', 's', 'l', 'r', 'b', 'lr', 'rr', 'br',
              'hh', 'ha', 'hs', 'he', 'ci', 'cw', 're', 'la', 'pl', 
              'u1', 'u2', 'u3', 'le', 'sa', 'mw', 't', 'pr', 'd', 'n', 'i',
              'v', 'nx', 'rp', 'u', 'f', 'ra', 'h', 'si']

#transform json list of dictionaries to csv 
with open('finale.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = class_info)
    writer.writeheader()
    writer.writerows(finaljson)


