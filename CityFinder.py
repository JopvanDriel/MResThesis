# -*- coding: utf-8 -*-
"""
This script aids in finding the geo_metro for each city, there are generally multiple IDs returned for
each city, so a manual inspection may be required to find the most effective choice. 
"""

import csv
import re

data = []
raw = []
temp2 = []
latlongs = []


#Read data from file
with open('C:\\Users\\Jop\\Documents\\Thesis\\10k_impressions_sample_US.csv', newline='', encoding='utf8') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
         raw.append(row)
         temp = row
         for i in range(len(temp)):
             #Find the column with geo_metro based on its proximity to geo_country
             if temp[i] == "USA":
                 temp2 = [temp[i+1]] 
             #find coordinates by regex matching
             elif re.match("-\d{2,3}\.\d*", temp[i]):
                 temp2.append(temp[i-1])
                 temp2.append(temp[i])
         if len(temp2)>1:
            data.append(temp2)
         temp2 = []
 
seattlelist = []
LAlist = []
SFlist = []
austinlist = []
NOlist = []
SDlist = []
bostonlist = []

#Search for coordinates close to the center of each city and store their geo_metro        
for i in range(len(data)):
    if re.match("47.*", data[i][1]) and re.match("-122.*", data[i][2]):
        if not data[i][0] in seattlelist:
            seattlelist.append(data[i][0])
    elif re.match("34.*", data[i][1]) and re.match("-118.*", data[i][2]):
        if not data[i][0] in LAlist:
            LAlist.append(data[i][0])
    elif re.match("37.*", data[i][1]) and re.match("-122.*", data[i][2]):
        if not data[i][0] in SFlist:
            SFlist.append(data[i][0])
    elif re.match("30.*", data[i][1]) and re.match("-97.*", data[i][2]):
        if not data[i][0] in austinlist:
            austinlist.append(data[i][0])
    elif re.match("29.*", data[i][1]) and re.match("-90.*", data[i][2]):
        if not data[i][0] in NOlist:
            NOlist.append(data[i][0])
    elif re.match("32.*", data[i][1]) and re.match("-117.*", data[i][2]):
        if not data[i][0] in SDlist:
            SDlist.append(data[i][0])
    elif re.match("42.*", data[i][1]) and re.match("-71.*", data[i][2]):
        if not data[i][0] in bostonlist:
            bostonlist.append(data[i][0])