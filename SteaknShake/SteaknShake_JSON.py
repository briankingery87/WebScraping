'''
-------------------------------------------------------------------------------
 Name:         SteaknShake_JSON.py

 Purpose:      Creates a file geodatabase containing a feature class with all
               SteaknShake locations.

 Author:       Brian Kingery

 Created:      8/12/2016
 Copyright:    (c) bkingery 2016

 Directions:   Ensure JSON file is still operational
               JSON - "http://www.steaknshake.com/api/locations_document"
               
 Website:      http://www.steaknshake.com
-------------------------------------------------------------------------------
'''

import urllib, json, csv, arcpy, datetime
from arcpy import env

def writeCSV(workarea,name,datalist):
    with open(workarea + '/' + name + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in datalist:
            try:
                writer.writerow(item)
            except UnicodeEncodeError:
                pass
    csvfile.close()
    print name + '.csv','created'
    
def createFileGeodatabase(workarea,gdbname):
    gdb = workarea + "/" + gdbname + ".gdb"
    if arcpy.Exists(gdb):
        arcpy.Delete_management(gdb)
    arcpy.CreateFileGDB_management(workarea, gdbname)
    print gdbname + '.gdb','created'
    
def createPoints(workarea,gdbname,csvname,fcname,latfield,longfield):
    input_table  = workarea + "/" + csvname + '.csv'
    output_points  = gdbname + ".gdb/" + fcname
    x_field  = longfield
    y_field  = latfield
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)
    print 'Point feature class created'

#-------------------------------------------------------------------------------

# let the big dawg eat
ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

## Target Locations
projectFolder = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/Development/Web_Scraping/SteaknShake"
env.workspace = projectFolder
env.overwriteoutput = True

DATA = []
## Column Headers for CSV file
columnID        = "ID"
columnName      = "Name"
columnAddress   = "Address"
columnCity      = "City"
columnState     = "State"
columnZipcode   = "Zipcode"
columnPhone     = "Phone"
columnLat       = "Latitude"
columnLon       = "Longitude"
columnType      = "Type"
columnURL       = "URL"
headers = columnID, columnName, columnAddress, columnCity, columnState, columnZipcode, columnPhone, columnLat, columnLon, columnType, columnURL
DATA.append(headers)
   
url = "http://www.steaknshake.com/api/locations_document"
htmlfile = urllib.urlopen(url)
data = json.load(htmlfile)

try:
    i=0
    while i<9999999999999999999999999999999999999:
        ID      = data[i]["id"]
        name    = data[i]["name"]
        address = data[i]["address1"]
        city    = data[i]["city"]
        state   = data[i]["state"]
        zipcode = data[i]["zip"]
        phone   = data[i]["phone"]
        lat     = data[i]["lat"]
        lon     = data[i]["lng"]
        type_   = data[i]["type"]
        url     = data[i]["snapfinger_url"]

        entry = ID, name, address, city, state, zipcode, phone, lat, lon, type_, url
        DATA.append(entry)
        
        i+=1
except:
    pass

geodatabaseName = 'SteaknShake'
csvName = 'SteaknShake_csv'
featureClassName = 'Restaraunt_Location'

writeCSV(projectFolder,csvName,DATA)
createFileGeodatabase(projectFolder,geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,columnLat,columnLon)

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]


