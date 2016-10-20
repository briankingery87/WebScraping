#-------------------------------------------------------------------------------
# Name:         NPS_GeoPDFs.py
#
# Purpose:      Download the GeoPDFs of all state parks. A folder on your
#               Desktop will be created called, NationalParkService
#
# Author:       Brian Kingery
#
# Created:      10/20/2016
# 
# Main website scraped: https://www.nps.gov/hfc/cfm/carto-atoz-geopdf.cfm?letter=a
#
#-------------------------------------------------------------------------------


import urllib, datetime, os, arcpy
from bs4 import BeautifulSoup
from urllib import urlopen

TodaysDate = datetime.datetime.today().strftime('%Y%m%d') # today's date in yyyymmdd format

folder = 'NationalParkService'
parkFolder = r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop' + os.sep + folder

##if arcpy.Exists(parkFolder):
##    arcpy.Delete_management(parkFolder)
##if not os.path.exists(parkFolder):
##    os.makedirs(parkFolder)

letters = 'abcdefghijklmnopqrstuvwxyz'
for letter in letters:
    html = urlopen('https://www.nps.gov/hfc/cfm/carto-atoz-geopdf.cfm?letter=' + letter)
    soup = BeautifulSoup(html, 'html.parser')
    for section in soup.find_all('ul'):
        
##        lis = section.find_all('li')
##        url = lis.get('href')
####        a = str(lis[0].get_text())
##        print url


##    html = urlopen('https://www.nps.gov/hfc/cfm/carto-atoz-geopdf.cfm?letter=' + letter)
##    soup = BeautifulSoup(html, 'html.parser')
##    for section in soup.findAll('ul'):
##        for p in section.findAll('li',{'id':'anch*'}):
##            print p

        
##        subfolderTitle = section.get('title').replace(" ","_").replace(".","")
##        subfolder = flagFolder + os.sep + subfolderTitle
##        os.makedirs(subfolder)
##        print 'Folder:',subfolderTitle


##for section in soup.findAll('a',{'class':'link-img-left'}):
##    link = section.get('href')
##    subfolderTitle = section.get('title').replace(" ","_").replace(".","")
##    subfolder = flagFolder + os.sep + subfolderTitle
##    os.makedirs(subfolder)
##    print 'Folder:',subfolderTitle
##    
##    newHTML = urlopen(link)
##    newSoup = BeautifulSoup(newHTML, 'html.parser')
##    for section in newSoup.findAll('a',{'class':'link-img-left'}):
##        picURL1 = section.findChildren()[0]
##        picURL = picURL1.get('src')
##        picTitle = section.get('title').replace(" ","_").replace(".","").replace("-","_")
##        urllib.urlretrieve(picURL, subfolder + os.sep + picTitle + '.jpg')
##        print '\tFlag:',picTitle
