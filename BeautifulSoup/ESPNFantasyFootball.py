# https://www.youtube.com/watch?v=BCJ4afDX4L4

import urllib, datetime, os
from bs4 import BeautifulSoup
from urllib import urlopen

TodaysDate = datetime.datetime.today().strftime('%Y%m%d') # today's date in yyyymmdd format

f = open(r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop\FFProjections.txt','w')

x = 0
while x < 500:
    html = urlopen('http://games.espn.go.com/ffl/tools/projections?startIndex=' + str(x))#.read()
    soup = BeautifulSoup(html, 'html.parser')
    tableStats = soup.find('table', {'class' : 'playerTableTable tableBody'})
    for row in tableStats.findAll('tr')[2:]:

        col = row.findAll('td')
        try:
            name = col[0].a.string.strip()
            f.write(name+'\n')
        except:# Exception as e:
            pass
    x+=40

f.close
