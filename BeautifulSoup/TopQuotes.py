# -*- coding: cp1252 -*-

# https://www.youtube.com/watch?v=0mAGb6sCZWc

from bs4 import BeautifulSoup
from urllib import urlopen

html = urlopen('https://litemind.com/best-famous-quotes')
soup = BeautifulSoup(html, 'html.parser')
for section in soup.findAll('div',{'class':'wp_quotepage'}):
    quote = section.findChildren()[0].renderContents().replace("’","'")
    author = section.findChildren()[1].renderContents().replace("—","\n")
    print quote, author
