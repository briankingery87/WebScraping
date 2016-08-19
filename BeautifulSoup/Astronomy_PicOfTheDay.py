import urllib, datetime, os
from bs4 import BeautifulSoup
from urllib import urlopen

TodaysDate = datetime.datetime.today().strftime('%Y%m%d') # today's date in yyyymmdd format

html = urlopen('http://apod.nasa.gov/apod/astropix.html')
soup = BeautifulSoup(html, 'html.parser')
for section in soup.findAll('img'):
    baseURL = 'http://apod.nasa.gov/apod/'
    picURL = section.get('src')
    urllib.urlretrieve(baseURL+picURL, r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop' + os.sep + 'Astronomy_PicOfTheDay_' + str(TodaysDate) + '.jpg')
