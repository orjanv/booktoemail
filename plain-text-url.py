#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, sys

#soup = BeautifulSoup(open("test.htm"), "html.parser")

url = 'http://www.gutenberg.org/ebooks/' + sys.argv[1]
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", text="Plain Text UTF-8")

for link in links:
    print 'http://' + link.attrs['href'][2:]
