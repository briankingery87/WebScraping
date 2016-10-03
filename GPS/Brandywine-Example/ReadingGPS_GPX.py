'''
-------------------------------------------------------------------------------
 Name:         ReadingGPS_GPX.py
 Purpose:      Creates a file geodatabase containing a feature class with a point
               feature class of waypoints and route points from the GPX file.
 Author:       Brian Kingery
 Created:      10/3/2016
 Copyright:    (c) bkingery 2016
 Website:      http://www.hikingupward.com/GWNF/BrandywineRecreationArea
 GPS eXchange (GPX) - http://www.hikingupward.com/GWNF/BrandywineRecreationArea/Brandywine.gpx
-------------------------------------------------------------------------------
'''

import urllib, csv, arcpy, datetime, os
import os.path as path
import xml.etree.ElementTree as ElementTree
import gpxpy, gpxpy.gpx
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
    columnType      = "Type"
    columnName      = "Name"
    columnLat       = "Latitude"
    columnLon       = "Longitude"
    headers = columnType, columnName, columnLat, columnLon
    datalist.append(headers)

    gpx_file = open(xmlfile, 'r')
    gpx = gpxpy.parse(gpx_file)

    for waypoint in gpx.waypoints:
##        print 'Waypoint --> {0} --> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude)
        _type = 'Waypoint'
        name  = waypoint.name
        lat   = waypoint.latitude
        lon   = waypoint.longitude

        entry = _type, name, lat, lon
        datalist.append(entry)

    for route in gpx.routes:
        for point in route.points:
##            print '----- Point --> {0} --> ({1},{2})'.format(point.name, point.latitude, point.longitude)
            _type = 'RoutePoint'
            name  = point.name
            lat   = point.latitude
            lon   = point.longitude

            entry = _type, name, lat, lon
            datalist.append(entry)

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

projectFolder    = r'C:\Users\bkingery\Desktop\Hike'
XML              = r'http://www.hikingupward.com/GWNF/BrandywineRecreationArea/Brandywine.gpx'
outputName       = 'Hiking'

xmlDocument      = outputName
geodatabaseName  = outputName
csvName          = outputName
featureClassName = outputName

createXML(projectFolder, XML, xmlDocument)
csvData = xmlParser(xmlDoc)
writeCSV(projectFolder, csvName, csvData)
createFileGeodatabase(projectFolder, geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,'Latitude','Longitude')

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]
