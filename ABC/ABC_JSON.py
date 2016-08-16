#-------------------------------------------------------------------------------
# Name:         ABC_JSON.py
#
# Purpose:      Creates a file geodatabase containing a feature class with all
#               Virginia ABC store locations.
#
# Author:       Brian Kingery
#
# Created:      4/27/2016
# Copyright:    (c) bkingery 2016
#
# Directions:   Ensure JSON file is still operational
#               JSON - https://www.abc.virginia.gov/api/stores/getAll
# Website:      https://www.abc.virginia.gov/about/find-a-store
#-------------------------------------------------------------------------------

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

def createPoints(workarea,gdbname,csvname,latfield,longfield):
    input_table  = workarea + "/" + csvname + '.csv'
    output_points  = gdbname + ".gdb/" + csvname
    x_field  = longfield
    y_field  = latfield
    input_format = 'DD_2'
    output_format = 'DD_2'
    id_field = ''
    spatial_ref = arcpy.SpatialReference('WGS 1984')
    arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref)
    print 'Point feature class created'

def createFileGeodatabase(workarea,gdbname):
    gdb = workarea + "/" + gdbname + ".gdb"
    if arcpy.Exists(gdb):
        arcpy.Delete_management(gdb)
    arcpy.CreateFileGDB_management(workarea, gdbname)
    print gdbname + '.gdb','created'

# let the big dawg eat
ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

## Target Locations
projectFolder = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/Development/Web_Scraping/ABC"
env.workspace = projectFolder
env.overwriteoutput = True

url = "https://www.abc.virginia.gov/api/stores/getAll"
#url = "https://www.abc.virginia.gov/api/stores/getAll?searchString=RICHMOND%2C+VA+23220&currentLatLng%5BLatitude%5D=37.5464259&currentLatLng%5BLongitude%5D=-77.46446069999999"
htmlfile = urllib.urlopen(url)
data = json.load(htmlfile)

DATA = []
## Column Headers for CSV file
columnStoreID   = "StoreID"
columnAddress   = "Address"
columnCity      = "City"
columnState     = "State"
columnZipcode   = "Zipcode"
columnPhone     = "Phone"
columnLat       = "Latitude"
columnLon       = "Longitude"
headers = columnStoreID, columnAddress, columnCity, columnState, columnZipcode, columnPhone, columnLat, columnLon
DATA.append(headers)

i=0
while i<len(data):
    storeID = data[i]["StoreId"]
    address = data[i]["Address"]["Address1"]
    city    = data[i]["Address"]["City"]
    state   = data[i]["Address"]["State"]
    zipcode = data[i]["Address"]["Zipcode"]
    phone   = data[i]["PhoneNumber"]["FormattedPhoneNumber"].replace(" ","").replace("(","").replace(")","").replace("-","")
    lat     = data[i]["Latitude"]
    lon     = data[i]["Longitude"]
    
    entry = storeID, address, city, state, zipcode, phone, lat, lon
    DATA.append(entry)
    i+=1

writeCSV(projectFolder,'ABC_Stores',DATA)
createFileGeodatabase(projectFolder,'VA_ABC')
createPoints(projectFolder,'VA_ABC','ABC_Stores',columnLat,columnLon)

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]


