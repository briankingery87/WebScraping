'''
-------------------------------------------------------------------------------
 Name:         MakePoints.py

 Purpose:      Creates a file geodatabase containing a feature class with all
               toxic release sites provided from EPA.

 Author:       Brian Kingery

 Created:      5/20/2016
 Copyright:    (c) bkingery 2016

 Website:      https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-2014
-------------------------------------------------------------------------------
'''

import arcpy, datetime
from arcpy import env
    
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

# GO
ExecutionStartTime = datetime.datetime.now()
print "Started: %s" % ExecutionStartTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Processing\n"

## Target Locations
projectFolder = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/EPA_Thesis/Data/EPA_Data"
env.workspace = projectFolder
env.overwriteoutput = True

geodatabaseName = 'My_US_TRI_2014'
csvName = 'My_TRI_2014_US'
featureClassName = 'US_2014_Sites'

createFileGeodatabase(projectFolder,geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,'LATITUDE','LONGITUDE')

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]

