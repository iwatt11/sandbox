import os
import urllib
import urllib2
from bs4 import BeautifulSoup

os.chdir('C:\Users\iwatt\PycharmProjects\Sandbox\Images')
url = "http://www.newyorker.com/humor"
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)
imgs = soup.findAll("img", {"class": "owl-lazy lazyOwl landscape  cartoon"})

for img in imgs:
    imgUrl = img['data-medium-src']
    imgName = os.path.basename(imgUrl)
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")
    filename = os.path.join(directory, imgName)
    urllib.urlretrieve(imgUrl, filename)