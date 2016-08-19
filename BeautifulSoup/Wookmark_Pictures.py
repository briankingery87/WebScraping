from bs4 import BeautifulSoup
from urllib import urlopen

html = urlopen('http://www.wookmark.com')
soup = BeautifulSoup(html, 'html.parser')

images = [img for img in soup.findAll('img')]
print (str(len(images)) + " images found.")
image_links = [each.get('src') for each in images]
for each in image_links:
    filename=each.split('/')[-1]
##    urllib.urlretrieve(each, filename)
    print filename
