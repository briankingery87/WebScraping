import arcpy, time
from arcpy import env

env.workspace = r"R:\Divisions\InfoTech\Private\GIS_Private\Kingery\EPA_Thesis\Data\EPA.gdb"
env.overwriteOutput = True

##fclist = arcpy.ListFeatureClasses()
##for fc in fclist:
##    print fc

##fc = 'TRI_2014_US'
fc = 'TRI_2014_ProjectSites'
field = 'TRI_FACILITY_ID'

##fieldlist = arcpy.ListFields(fc)
##for field in fieldlist:
##    print field.name

uniqueList = []
count = 0
with arcpy.da.SearchCursor(fc, [field]) as cursor:
    for row in cursor:
        uniqueList.append(row[0])
        count+=1
del cursor

unique_word_count = len(set(uniqueList))

print 'Total Facilities'
print unique_word_count
print 'Total Records'
print count





