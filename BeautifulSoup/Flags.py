#-------------------------------------------------------------------------------
# Name:         Flags.py
#
# Purpose:      Download the flags of nations across the world. A folder on your
#               Desktop will be created called, Flag_Download_Folder
#
# Author:       Brian Kingery
#
# Created:      9/30/2016
# 
# Main website scraped: http://mapshop.com/flags/flags.htm
#
#-------------------------------------------------------------------------------


import urllib, datetime, os, arcpy
from bs4 import BeautifulSoup
from urllib import urlopen

TodaysDate = datetime.datetime.today().strftime('%Y%m%d') # today's date in yyyymmdd format

folder = 'Flag_Download_Folder'
flagFolder = r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop' + os.sep + folder

if arcpy.Exists(flagFolder):
    arcpy.Delete_management(flagFolder)
if not os.path.exists(flagFolder):
    os.makedirs(flagFolder)

html = urlopen('http://mapshop.com/flags/flags.htm')
soup = BeautifulSoup(html, 'html.parser')
for section in soup.findAll('a',{'class':'link-img-left'}):
    link = section.get('href')
    subfolderTitle = section.get('title').replace(" ","_").replace(".","")
    subfolder = flagFolder + os.sep + subfolderTitle
    os.makedirs(subfolder)
    print 'Folder:',subfolderTitle
    
    newHTML = urlopen(link)
    newSoup = BeautifulSoup(newHTML, 'html.parser')
    for section in newSoup.findAll('a',{'class':'link-img-left'}):
        picURL1 = section.findChildren()[0]
        picURL = picURL1.get('src')
        picTitle = section.get('title').replace(" ","_").replace(".","").replace("-","_")
        urllib.urlretrieve(picURL, subfolder + os.sep + picTitle + '.jpg')
        print '  Flag:',picTitle
