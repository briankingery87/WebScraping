'''
-------------------------------------------------------------------------------
 Name:         CraftBeer_XML.py

 Purpose:      Creates a file geodatabase containing a feature class with all
               breweries kept on file at CraftBeer.com

 Author:       Brian Kingery

 Created:      5/3/2016
 Copyright:    (c) bkingery 2016

 Directions:   Ensure XML file is still operational
               XML - http://www.craftbeer.com/wp-content/uploads/ba-us.xml
 Website:      http://www.craftbeer.com
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
    columnID        = "ID"
    columnCompany   = "Company"
    columnAddress   = "Address"
    columnCity      = "City"
    columnState     = "State"
    columnZipcode   = "Zipcode"
    columnCountry   = "Country"
    columnPhone     = "Phone"
    columnMType     = "Member_Type"
    columnType      = "Type"
    columnURL       = "URL"
    columnLat       = "Latitude"
    columnLon       = "Longitude"
    headers = columnID, columnCompany, columnAddress, columnCity, columnState, columnZipcode, columnCountry, columnPhone, columnMType, columnType, columnURL, columnLat, columnLon
    datalist.append(headers)

    i=0
    tree = ElementTree.parse(xmlfile)
    for node in tree.findall('marker'):
        ID      = node.attrib.get('id')
        company = node.attrib.get('company')
        address = node.attrib.get('address')
        city    = node.attrib.get('city')
        state   = node.attrib.get('state')
        zipcode = node.attrib.get('zip')
        country = node.attrib.get('country')
        #phone   = data["ProviderFinderResult"][i]["Phone"].replace(" ","").replace("(","").replace(")","").replace("-","")
        phone   = node.attrib.get('phone')
        mType   = node.attrib.get('member_type')
        _type   = node.attrib.get('type')
        url     = node.attrib.get('url')
        lat     = node.attrib.get('lat')
        lon     = node.attrib.get('lng')

        entry = ID, company, address, city, state, zipcode, country, phone, mType, _type, url, lat, lon
        datalist.append(entry)
        i+=1

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

projectFolder    = 'R:/Divisions/InfoTech/Private/GIS_Private/Kingery/Development/Web_Scraping/CraftBeer'
craftBeerXML     = 'http://www.craftbeer.com/wp-content/uploads/ba-us.xml'
outputName       = 'CraftBeer'

xmlDocument      = outputName
geodatabaseName  = outputName
csvName          = outputName
featureClassName = outputName

createXML(projectFolder, craftBeerXML, xmlDocument)
csvData = xmlParser(xmlDoc)
writeCSV(projectFolder, csvName, csvData)
createFileGeodatabase(projectFolder, geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,'Latitude','Longitude')

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]











