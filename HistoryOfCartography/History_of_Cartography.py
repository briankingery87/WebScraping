#-------------------------------------------------------------------------------
# Name:         History_of_Cartography.py
#
# Purpose:      Download and combine all PDFs for the first 3 volumes of The
#               History of Cartography
#
# Author:       Brian Kingery
#
# Created:      8/22/2016
# 
# The History of Cartography
# http://www.press.uchicago.edu/books/HOC/index.html
#-------------------------------------------------------------------------------

import urllib, os, arcpy, glob
from bs4 import BeautifulSoup
from urllib import urlopen

Desktop = r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop'
MainFolder = Desktop + os.sep +'History_of_Cartography'
VOL1Folder = MainFolder + os.sep + 'VOLUME1'
VOL2Folder = MainFolder + os.sep + 'VOLUME2'
VOL2Book1Folder = VOL2Folder + os.sep + 'Book1'
VOL2Book2Folder = VOL2Folder + os.sep + 'Book2'
VOL2Book3Folder = VOL2Folder + os.sep + 'Book3'
VOL3Folder = MainFolder + os.sep + 'VOLUME3'
VOL3Part1Folder = VOL3Folder + os.sep + 'Part1'
VOL3Part2Folder = VOL3Folder + os.sep + 'Part2'

if arcpy.Exists(MainFolder):
    arcpy.Delete_management(MainFolder)
os.makedirs(MainFolder)
os.makedirs(VOL1Folder)
os.makedirs(VOL2Folder)
os.makedirs(VOL2Book1Folder)
os.makedirs(VOL2Book2Folder)
os.makedirs(VOL2Book3Folder)
os.makedirs(VOL3Folder)
os.makedirs(VOL3Part1Folder)
os.makedirs(VOL3Part2Folder)

##############################################################################

VOLUME1 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V1/Volume1.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-12] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME1[TITLE] = PDF                                    #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME1[TITLE] = PDF                                    #Add to dictionary
    i+=1
    
##for key, value in VOLUME1.iteritems():
##    print 'Title: ', key
##    print 'PDF:   ', value
    
for x in VOLUME1:
    urllib.urlretrieve(VOLUME1[x], VOL1Folder + os.sep + x + '.pdf')

VOL1_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL1.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL1_FinalPDF)

Volume1PDFs = glob.glob(VOL1Folder + os.sep + '*.pdf')
for pdf in Volume1PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL1.pdf compiling'

################################################################################

VOLUME2Book1 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V2_B1/Volume2_Book1.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-18] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME2Book1[TITLE] = PDF                               #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME2Book1[TITLE] = PDF                               #Add to dictionary
    i+=1
      
for x in VOLUME2Book1:
    urllib.urlretrieve(VOLUME2Book1[x], VOL2Book1Folder + os.sep + x + '.pdf')

VOL2Book1_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL2_Book1.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL2Book1_FinalPDF)

Volume2Book1PDFs = glob.glob(VOL2Book1Folder + os.sep + '*.pdf')
for pdf in Volume2Book1PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL2_Book1.pdf compiling'

################################################################################

VOLUME2Book2 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V2_B2/Volume2_Book2.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-18] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME2Book2[TITLE] = PDF                               #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME2Book2[TITLE] = PDF                               #Add to dictionary
    i+=1
   
for x in VOLUME2Book2:
    urllib.urlretrieve(VOLUME2Book2[x], VOL2Book2Folder + os.sep + x + '.pdf')

VOL2Book2_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL2_Book2.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL2Book2_FinalPDF)

Volume2Book2PDFs = glob.glob(VOL2Book2Folder + os.sep + '*.pdf')
for pdf in Volume2Book2PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL2_Book2.pdf compiling'

################################################################################

VOLUME2Book3 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V2_B3/Volume2_Book3.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-18] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME2Book3[TITLE] = PDF                               #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME2Book3[TITLE] = PDF                               #Add to dictionary
    i+=1
  
for x in VOLUME2Book3:
    urllib.urlretrieve(VOLUME2Book3[x], VOL2Book3Folder + os.sep + x + '.pdf')

VOL2Book3_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL2_Book3.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL2Book3_FinalPDF)

Volume2Book3PDFs = glob.glob(VOL2Book3Folder + os.sep + '*.pdf')
for pdf in Volume2Book3PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL2_Book3.pdf compiling'

################################################################################

VOLUME3Part1 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V3_Pt1/Volume3_Part1.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-18] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME3Part1[TITLE] = PDF                               #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME3Part1[TITLE] = PDF                               #Add to dictionary
    i+=1
    
for x in VOLUME3Part1:
    urllib.urlretrieve(VOLUME3Part1[x], VOL3Part1Folder + os.sep + x + '.pdf')

VOL3Part1_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL3_Part1.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL3Part1_FinalPDF)

VOL3Part1PDFs = glob.glob(VOL3Part1Folder + os.sep + '*.pdf')
for pdf in VOL3Part1PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL3_Part1.pdf compiling'

################################################################################

VOLUME3Part2 = {}

url = 'http://www.press.uchicago.edu/books/HOC/HOC_V3_Pt2/Volume3_Part2.html'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
i=1
for item in soup.findAll('span',{'class':'chapter'}):
    href = item.find('a')
    pdfURL = href.get('href')

    PDF = url[:-18] + pdfURL                                    #URL for pdf
    title = item.get_text().replace("\n","").replace(":","").replace("'","").replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","_")    #Title of Chapter
    if i<10:
        TITLE = str(0) + str(i) + '_' + title                   #Formatted Title
        VOLUME3Part2[TITLE] = PDF                               #Add to dictionary
    else:
        TITLE = str(i) + '_' + title                            #Formatted Title
        VOLUME3Part2[TITLE] = PDF                               #Add to dictionary
    i+=1
    
for x in VOLUME3Part2:
    urllib.urlretrieve(VOLUME3Part2[x], VOL3Part2Folder + os.sep + x + '.pdf')

VOL3Part2_FinalPDF = MainFolder + os.sep + 'History_of_Cartography_VOL3_Part2.pdf'
finalPDF = arcpy.mapping.PDFDocumentCreate(VOL3Part2_FinalPDF)

VOL3Part2PDFs = glob.glob(VOL3Part2Folder + os.sep + '*.pdf')
for pdf in VOL3Part2PDFs:
    finalPDF.appendPages(pdf)
print 'History_of_Cartography_VOL3_Part2.pdf compiling'

################################################################################
