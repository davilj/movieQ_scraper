#read all poster movie data files from a dir and create a list of the movie ids
#Each dir would be a year
#Use names in lamba function to

import sys
import os
import uuid
from random import randint

movieList = []

posterDir = sys.argv[1]
destDir = sys.argv[2]
print 'BuildGamePoster: ' + posterDir

def extractNames(posterFile):
    print "Testing: " + posterFile
    if (posterFile.endswith(".json")):
        print "----------------------------> found json file"
        moviePosterId = posterFile.replace(".json","")
        movieList.append(moviePosterId)

def readPosterDB(dirWithPosterInfo):
    for dirpath, dnames, fnames in os.walk(dirWithPosterInfo):
        for f in fnames:
            extractNames(f)

def save2PosterData(dest):
    import json
    fileName = dest + "/" + posterDir + "posters.json"
    f = open(fileName, 'w')
    f.write(json.dumps(movieList))
    f.flush()
    f.close()


readPosterDB(posterDir)
save2PosterData(destDir)
