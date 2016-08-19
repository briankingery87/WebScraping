import urllib, datetime, os
from bs4 import BeautifulSoup
from urllib import urlopen

TodaysDate = datetime.datetime.today().strftime('%Y%m%d') # today's date in yyyymmdd format

html = urlopen('http://epod.usra.edu/')
soup = BeautifulSoup(html, 'html.parser')
for section in soup.findAll('a',{'class':'asset-img-link'}):
    picURL = section.get('href')
    urllib.urlretrieve(picURL, r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop' + os.sep + 'EarthScience_PicOfTheDay' + str(TodaysDate) + '.jpg')
