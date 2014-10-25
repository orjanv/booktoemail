#!/usr/bin/env python
import oauth2 as oauth
import urlparse, urllib, urllib2, os, sys
import xml.etree.ElementTree as ET

# Set up some variables
CONSUMER_KEY = 'LAe3blOt1IpgcJuJpqGzQ'
#MY_USER_ID = '2686518'

def FindBookID(query):
	url_base = "http://www.goodreads.com/search.xml"
	params = {'key':CONSUMER_KEY, 'q':query}
	encoded_params = urllib.urlencode(params)
	url = url_base + '?' + encoded_params
	response = urllib2.urlopen(url)
	search_result = response.read()

	# Write XML content to file
	xmlfile = 'search_result.xml'
	f = open(xmlfile, 'w')
	f.write(search_result)
	f.close()

	# Set up the element tree from the XML file
	tree = ET.parse(xmlfile)
	root = tree.getroot()

	# Build a list of names based on the <name> tag in the xml file
	search_result_dict = {}
	for books in root.find('search'):
		for bookcount in books.iter('best_book'):
			book_title = bookcount.find('title').text
			book_image_url = bookcount.find('image_url').text
			for author in bookcount.iter('author'):
				book_author = author.find('name').text
			book_id = bookcount.find('id').text
			search_result_dict[book_id] = (book_title,book_author, book_image_url)
			
	return search_result_dict.values()[0][2]


def main():
	try:
		print FindBookID(sys.argv[1])
		exit(1)
	except IndexError:
		exit(1)
	
if __name__ == '__main__':
    main()
