
import os
filelist = [] #Initialize list of files in directory

#Get a list of all .xml files in directory
for file in os.listdir(os.getcwd()):
    if file.endswith(".xml"):
        filelist.append(file)


pointslist = [100, 90, 81, 73, 66, 60, 55, 51, 47, 44, 41, 39, 37, 36, 35, 34,
              33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18,
              17, 16, 15, 14, 13, 12, 11]
pointslist2 = [10] * 60
pointslist.extend(pointslist2)
pointslist.append(5)
pointslist.reverse()

racenumlist = ["name"]

namelistm = [{}] #Initialize dictionary list of names and race results
namelistw = [{}]

#Get the list of women names
women = open('women.txt', 'r')
womenlist = women.read().split('\n')
women.close()

import xml.etree.ElementTree as ET

# Load each file and make string for the race number
for i, file in enumerate(filelist):
    tree = ET.parse(file)
    root = tree.getroot()
    racenumstr = "race" + str(i+1)
    racenumlist.append(racenumstr)
    
    pointslistm = list(pointslist)
    pointslistw = list(pointslist)

    for ClassResult in root.find("ClassResult"):
        #iterate over all the person results
        for PersonResult in ClassResult.iter("PersonResult"):
            namestr = ""
            x = 0 # A variable to keep track of whether the runner's name already exists in namelist

            
            for Given in PersonResult.iter("Given"):
                namestr = namestr + Given.text + " "
            
            for Family in PersonResult.iter("Family"):
                namestr = namestr + Family.text #namestr now contains entire name of person
                     
            if namestr in womenlist:
                
                for entry in namelistw:
                
                    #search namelist for prior entry with the same name
                    if namestr in entry.values(): #if there is one, add raceposval to the dictionary
                        entry[racenumstr] = pointslistw.pop()
                        x = 1
                    
                if x == 0:
                    #if not, append namelist with a new entry, including name and race position
                    namelistw.append({"name":namestr, 
                                racenumstr:pointslistw.pop()})
                
            else:
                for entry in namelistm:
                
                    #search namelist for prior entry with the same name
                    if namestr in entry.values(): #if there is one, add raceposval to the dictionary
                        entry[racenumstr] = pointslistm.pop()
                        x = 1
                    
                if x == 0:
                    #if not, append namelist with a new entry, including name and race position
                    namelistm.append({"name":namestr, 
                                racenumstr:pointslistm.pop()})

from operator import itemgetter
            
for entry in namelistm:
    best10m = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:11])
    # sorts all dictionary values into a list. The text entry (person's name) is first
    # the best 10 points values are 1 - 11 in the list. they are stored in the dictionary
    # best10
    entry['sumbest10'] = sum(best10m.itervalues())
    #sum of the 10 best entries is added to each runners dictionary under the entry "sumbest10"

for entry in namelistw:
    best10w = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:11])
    # sorts all dictionary values into a list. The text entry (person's name) is first
    # the best 10 points values are 1 - 11 in the list. they are stored in the dictionary
    # best10
    entry['sumbest10'] = sum(best10w.itervalues())
    #sum of the 10 best entries is added to each runners dictionary under the entry "sumbest10"

racenumlist.append('sumbest10') 
#adds the sumbest10 entry title to racenumlist for inclusion in csv output

import csv
#write output .csv file.
outfile = open("output.csv", "w")
w = csv.DictWriter(outfile, fieldnames = racenumlist, 
                   restval=0, extrasaction='ignore', dialect='excel')

for entry in namelistm:
    w.writerow(entry)
for entry in namelistw:
    w.writerow(entry)
outfile.close()
