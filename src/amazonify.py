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
            print extractProp(f)
            break

def populateMovieList():
    for key in movieDB.keys():
        props = movieDB[key]
        movieList.append(props[0])

def buildFileProp():
    numberOfMovies = len(movieList)
    print "NumberOfM: " + str(numberOfMovies)
    for key in movieDB.keys():
        x=[randint(0,numberOfMovies) for p in range(0,15)]
        otherNames = []
        for number in x:
            name = movieList[number]
            if (len(otherNames)<10 and name!=key):
                otherNames.append(name)
        print otherNames


populateMovieDB(movieDir)
populateMovieList()
buildFileProp()
