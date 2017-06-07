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


movieDB = {}
movieList = []

movieDir = sys.argv[1]
destDir = sys.argv[2]
print 'amazonfy movies in: ' + movieDir

def extractProp(mailFile):
    nameKey = mailFile.replace(".jpg","")
    name = nameKey.replace("_"," ")
    value = (name, uuid.uuid4().urn[9:])
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
            for index in range(0,5):
                newSrc = key + "_" + str(index) + '.jpg'
                fileSrc_ = os.path.join(dirpath, newSrc)
                newDestination = newSrc.replace(key, values[1])
                fileDest_ = os.path.join(toDir, newDestination)
                posters.append(fileDest_)
                print fileSrc_
                print fileDest_
                os.rename(fileSrc_, fileDest_)

            makeMovieFile(toDir, values, posters, fileDest)
            break






populateMovieDB(movieDir)
populateMovieList()
buildFileProp()

makeAmazonFiles(movieDir, destDir)
