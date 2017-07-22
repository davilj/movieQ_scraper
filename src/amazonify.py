#read all movies in a dir and create a movie file:
#var movie =  {
#      name:'Rams',
#      names:['Rams','Star wars', 'Here comes the boom', 'Grownups', 'American Pie', 'Up', 'Wally', 'Lion King', 'Tron', 'Lord of the Rings'],
#      posters: ['movies/Rams_0.jpg', 'movies/Rams_1.jpg', 'movies/Rams_2.jpg', 'movies/Rams_3.jpg', 'movies/Rams_4.jpg', 'movies/Rams.jpg' ]
#    };
#
# also create a flat file structure with the files in it
# each movie generates
#   movie file
#   list of encoded images

import sys
import os
import uuid
from random import randint
import json

#main db, store key {name with underscore : (name:code)}
movieDB = {}
movieList = []
movieDict = {}
scoreDB = {}

movieDir = sys.argv[1]
destDir = sys.argv[2]
print 'amazonfy movies in: ' + movieDir

#random int, check if already in movie db
def getKey():
    while True:
        randomInt = randint(0, 32000)
        #change this for each year
        key = 'p16_' + str(randomInt)
        if not (key in movieDB):
            return key

def extractProp(mailFile):
    nameKey = mailFile.replace(".jpg","")
    name = nameKey.replace("_"," ")
    value = (name, getKey())
    movieDB[nameKey]=value
    return (nameKey, value)

def populateMovieDB(dirWithMovieDirs):
    for dirpath, dnames, fnames in os.walk(dirWithMovieDirs):
        for f in fnames:
            extractProp(f)
            break

def populateMovieList():
    for key in movieDB.keys():
        props = movieDB[key]
        movieList.append(props[0])

def buildFileProp():
    numberOfMovies = len(movieList)
    print "NumberOfM: " + str(numberOfMovies)
    for key in movieDB.keys():
        x=[randint(0,numberOfMovies-1) for p in range(0,15)]
        otherNames = []
        for number in x:
            name = movieList[number]
            if (len(otherNames)<10 and name!=key):
                otherNames.append(name)
        value = movieDB[key]
        movieDB[key]=(value[0], value[1], otherNames)

def extractKey(fileName):
    newName = fileName.replace('.jpg','')
    for e in range(0,5):
        endPart = '_' + str(e)
        if newName.endswith(endPart):
            newName = newName.replace(endPart,'')
            break
    return newName

def makeMovieFile(toDir, values, posters, mainFile):
    import json
    posters.append(mainFile)
    jsonDict = {}
    jsonDict['name']=values[0]
    jsonDict['names']=values[2]
    jsonDict['posters']=posters
    jsonFile = json.dumps(jsonDict)
    fileName = values[1] + ".json"
    f = open(fileName, 'w')
    f.write(json.dumps(jsonDict))
    f.flush()
    f.close()
    print jsonFile

def buildMovieDict():
    for key in movieDB.keys():
        value = movieDB[key]
        movieDict[value[1]]=value[0]
        scoreDB[value[1]]=0


def makeAmazonFiles(fromDir, toDir):
    os.mkdir(toDir)
    for dirpath, dnames, fnames in os.walk(fromDir):
        for f in fnames:
            fileSrc = os.path.join(dirpath,f)
            key = f.replace('.jpg','')
            values = movieDB[key]
            newFile = f.replace(key, values[1])
            fileDest = os.path.join(toDir, newFile)
            os.rename(fileSrc, fileDest)
            posters = []

            #makeMovieFile(toDir, values, posters, fileDest)
            break

def writeObject(object,name):
    f = open(name, 'w')
    f.write(json.dumps(object))
    f.flush()
    f.close()

populateMovieDB(movieDir)
populateMovieList()
buildFileProp()
buildMovieDict()
writeObject(scoreDB,"scoreDB")
writeObject(movieDict,"movieDict")

makeAmazonFiles(movieDir, destDir)
