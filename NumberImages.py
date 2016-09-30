import urllib, os, arcpy

folder = 'DeepLearningNeuralNet'
picFolder = r'C:\Users' + os.sep + os.environ['USERNAME'] + os.sep + 'Desktop' + os.sep + folder

##if os.path.exists(picFolder):
##    os.remove(picFolder)
##    os.makedirs(picFolder)
##else:
##    os.makedirs(picFolder)


if arcpy.Exists(picFolder):
    arcpy.Delete_management(picFolder)
if not os.path.exists(picFolder):
    os.makedirs(picFolder)

x=0
while x < 100:
    pic = 'http://sex-offender.vsp.virginia.gov/sor/captcha.jpg'
    urllib.urlretrieve(pic, picFolder + os.sep + 'Pic_' + str(x) + '.jpg')
    x+=1



