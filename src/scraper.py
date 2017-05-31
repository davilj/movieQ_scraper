#scrape movies for a specific year

from urllib2 import Request, urlopen

import sys
from bs4 import BeautifulSoup
import re
import os


year = sys.argv[1]
print 'loading movies for: ' + year

yearInfo = year + '_movies'

def download(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read()

def splitInto(location, name, ext, rows, columns):
    imgLocation = location + "/" + name + "." + ext
    from PIL import Image
    from random import shuffle
    catIm = Image.open(imgLocation)
    width, height = catIm.size
    #print width, height
    stepX = width/columns
    stepY = height/rows
    #print stepX, stepY
    count=0
    ids = range(0, (rows * columns))
    shuffle(ids)
    #print ids
    for xValue in range(0, (columns*stepX), stepX):
        #print "x-" + str(xValue)
        for yValue in range(0, (rows*stepY), stepY):
            #print "y-" + str(yValue)
            part = catIm.crop((xValue,yValue, xValue+stepX, yValue+stepY))
            part.save(location + "/" + name + "_" + str(ids[count]) + "." + ext)
            count = count + 1

#download page
url = 'http://www.wildaboutmovies.com/' + yearInfo + '/'
print 'downloading: ' + url
webpage = download(url)
print 'completed'

#soup
print 'parsing....'
soup = BeautifulSoup(webpage, "html.parser")
for movie in soup.find_all("img", class_="lazy"):
        name=movie['alt']
        posterS=movie['data-original']
        link = "http://www.wildaboutmovies.com" + movie.parent['href']
        print name
        print posterS
        detailWeb = download(link)
        detail = BeautifulSoup(detailWeb, "html.parser")
        imgUrl = detail.find("img", class_='wp-post-image')['src']
        print imgUrl

        poster = download(imgUrl)
        location=name.replace(" ", "_")
        os.mkdir(location)
        imageName = location + "/" + location + ".jpg"
        with open(imageName, "wb") as movieImg:
            movieImg.write(poster)
        splitInto(location, location, "jpg",4,4)
        #:break
        print "-----------------------------------------"
