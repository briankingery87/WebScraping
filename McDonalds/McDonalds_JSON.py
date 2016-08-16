'''
-------------------------------------------------------------------------------
 Name:         McDonalds_JSON.py

 Purpose:      Creates a file geodatabase containing a feature class with all
               McDonalds locations.

 Author:       Brian Kingery

 Created:      8/16/2016
 Copyright:    (c) bkingery 2016

 Directions:   Ensure JSON file is still operational
               JSON - "https://www.mcdonalds.com/services/mcd/us/restaurantLocator?latitude=39.833&longitude=-98.583&radius=10000&maxResults=1000&country=us&language=en-us"
               
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
projectFolder = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/Development/Web_Scraping/McDonalds"
env.workspace = projectFolder
env.overwriteoutput = True

DATA = []
## Column Headers for CSV file

columnName      = "Name"
columnURL       = "URL"
columnID        = "ID"
columnSiteID    = "Site_ID"
columnNatlID    = "Natl_ID"
columnRegionID  = "Reg_ID"
columnTVMarket  = "TV_Market"
columnTVMarketID = "TV_Market_ID"
columnAddress   = "Address"
columnCity      = "City"
columnState     = "State"
columnZipcode   = "Zipcode"
columnCountry   = "Country"
columnPhone     = "Phone"
columnLat       = "Latitude"
columnLon       = "Longitude"

headers = columnName,columnURL,columnID,columnSiteID,columnNatlID,columnRegionID,columnTVMarket,columnTVMarketID,columnAddress,columnCity,columnState,columnZipcode,columnCountry,columnPhone,columnLat,columnLon
DATA.append(headers)

##Lat/Long of center of US
##(39.833, -98.583)

Latitude  = 39.833
Longitude = -98.583
Radius = 10000000000
Results = 99999

CountryList = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'XK', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SS', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW', 'CS', 'AN']

for country in CountryList:
    try:
        url = "https://www.mcdonalds.com/services/mcd/us/restaurantLocator?latitude=" + str(Latitude) + "&longitude=" + str(Longitude) + "&radius=" + str(Radius) + "&maxResults=" + str(Results) + "&country=" + country.lower() + "&language=en-us"
        htmlfile = urllib.urlopen(url)
        data = json.load(htmlfile)
        i=0
        while i<Results:
            name    = "McDonalds"
            url     = data["features"][i]["properties"]["jobUrl"]
            ID         = data["features"][i]["properties"]["id"]
            siteID     = data["features"][i]["properties"]["identifiers"]["storeIdentifier"][0]["identifierValue"]
            NatlID     = data["features"][i]["properties"]["identifiers"]["storeIdentifier"][1]["identifierValue"]
            RegionID   = data["features"][i]["properties"]["identifiers"]["storeIdentifier"][2]["identifierValue"]
            TVMarket   = data["features"][i]["properties"]["identifiers"]["storeIdentifier"][5]["identifierValue"]
            TVMarketID = data["features"][i]["properties"]["identifiers"]["storeIdentifier"][6]["identifierValue"]
            address = data["features"][i]["properties"]["addressLine1"]
            city    = data["features"][i]["properties"]["addressLine3"]
            state   = data["features"][i]["properties"]["subDivision"]
            zipcode = data["features"][i]["properties"]["postcode"]
            country = data["features"][i]["properties"]["addressLine4"]
            phone   = data["features"][i]["properties"]["telephone"].replace(" ","").replace("(","").replace(")","").replace("-","")
            lat     = data["features"][i]["geometry"]["coordinates"][1]
            lon     = data["features"][i]["geometry"]["coordinates"][0]
        
            entry = name, url, ID, siteID, NatlID, RegionID, TVMarket, TVMarketID, address, city, state, zipcode, country, phone, lat, lon
            DATA.append(entry)
            i+=1
    except:
        pass

geodatabaseName = 'McDonalds'
csvName = 'McDonalds_csv'
featureClassName = 'McDonalds_Locations'

writeCSV(projectFolder,csvName,DATA)
createFileGeodatabase(projectFolder,geodatabaseName)
createPoints(projectFolder,geodatabaseName,csvName,featureClassName,columnLat,columnLon)

ExecutionEndTime = datetime.datetime.now()
ElapsedTime = ExecutionEndTime - ExecutionStartTime
print "\nEnded: %s" % ExecutionEndTime.strftime('%A, %B %d, %Y %I:%M:%S %p')
print "Elapsed Time: %s" % str(ElapsedTime).split('.')[0]











##print name
##print url 
##print ID  
##print siteID
##print NatlID
##print RegionID   
##print TVMarket   
##print TVMarketID 
##print address
##print city   
##print state  
##print zipcode
##print country 
##print phone   
##print lat     
##print lon
