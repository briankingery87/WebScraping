'''
-------------------------------------------------------------------------------
 Name:         SuperfundSites_XML.py

 Purpose:      Creates a file geodatabase containing a feature class with all
               Superfund sites provided by the EPA.

 Author:       Brian Kingery

 Created:      6/1/2016
 Copyright:    (c) bkingery 2016

 Directions:   Ensure XML file is still operational
               XML - https://www.epa.gov/sites/production/files/2015-08/nplfin.xml
 Website:      https://www.epa.gov/superfund/national-priorities-list-npl-sites-site-name
-------------------------------------------------------------------------------
'''

import urllib, csv, arcpy, datetime
import os.path as path
import xml.etree.ElementTree as ElementTree
from arcpy import env
from time import strftime

def createXML(workarea,url,name):
    global xmlDoc
    xmlDoc = name +'_'+strftime('%Y%m%d')+'.xml'
    xml_file = path.join(workarea, xmlDoc)
    urllib.urlretrieve(url, xml_file)
    print 'Retrieved:',xmlDoc

def xmlParser(xmlfile):
    datalist = []
    # column headers for CSV file
    siteName    = "Name"
    siteID      = "Site_EPA_ID"
    listingDate = "Listing_Date"
    siteScore   = "Site_Score"
    siteCity    = "City"
    siteState   = "State"
    siteLat     = "Latitude"
    siteLon     = "Longitude"
    headers = siteName, siteID, listingDate, siteScore, siteCity, siteState, siteLat, siteLon
    datalist.append(headers)    

    i=0
    while i<99999999999:
        try:
            tree = ElementTree.parse(xmlfile)
            root = tree.getroot()
            name  = root.getchildren()[i].getchildren()[0].text
            ID    = tree.findall('S')[i].attrib.get('E')
            date  = tree.findall('S')[i].attrib.get('F')
            score = tree.findall('S')[i].attrib.get('O')
            city  = tree.findall('S')[i].attrib.get('L')
            st    = tree.findall('S')[i].attrib.get('A')
            lat   = tree.findall('S')[i].attrib.get('J')
            lon   = tree.findall('S')[i].attrib.get('K')

            entry = name, ID, date, score, city, st, lat, lon
            datalist.append(entry)
            i+=1
        except:
            break
    print 'Items:    ',i
    return datalist
    

def writeCSV(workarea,name,datalist):
    with open(workarea + '/' + name +'_'+strftime('%Y%m%d')+'.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in datalist:
            try:
                writer.writerow(item)
            except UnicodeEncodeError:
                pass
    csvfile.close()
    print 'Created:  ',name +'_'+strftime('%Y%m%d')+'.csv'
    
def createFileGeodatabase(workarea,gdbname):
    gdb = gdbname +'_'+strftime('%Y%m%d')+'.gdb'
    gdbCheck = workarea + '/' + gdbname +'_'+strftime('%Y%m%d')+'.gdb'
    if arcpy.Exists(gdbCheck):
        arcpy.Delete_management(gdbCheck)
    arcpy.CreateFileGDB_management(workarea, gdb)
    print 'Created:  ',gdbname +'_'+strftime('%Y%m%d')+'.gdb'
    
def createPoints(workarea,gdbname,csvname,fcname,latfield,longfield):
    input_table  = workarea + '/' + csvname +'_'+strftime('%Y%m%d')+'.csv'
    output_points  = gdbname +'_'+strftime('%Y%m%d')+'.gdb/' + fcname+'_'+strftime('%Y%m%d')
    x_field  = longfield
    y_field  = latfield
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)
    print 'Created:   Point feature class'

#-------------------------------------------------------------------------------

ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

projectFolder    = 'R:/Divisions/InfoTech/Private/GIS_Private/Kingery/EPA_Thesis/Superfund'
superfundXML     = 'https://www.epa.gov/sites/production/files/2015-08/nplfin.xml'
outputName       = 'Superfund'

xmlDocument      = outputName
geodatabaseName  = outputName
csvName          = outputName
featureClassName = outputName

createXML(projectFolder, superfundXML, xmlDocument)
csvData = xmlParser(xmlDoc)
writeCSV(projectFolder, csvName, csvData)
createFileGeodatabase(projectFolder, geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,'Latitude','Longitude')

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]











