#scrape movies for a specific year

from urllib2 import Request, urlopen

import sys
from bs4 import BeautifulSoup
import re

year = sys.argv[1]
print 'loading movies for: ' + year

yearInfo = year + '_movies'

#create dir

#download page
url = 'http://www.wildaboutmovies.com/' + yearInfo + '/'
print 'downloading: ' + url
#use request and headers , mimmic browser (I'm not a robot)
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
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
        print link
        print "-----------------------------------------"
