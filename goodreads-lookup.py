#!/usr/bin/env python
import oauth2 as oauth
import urlparse, urllib, urllib2, os, sys
import xml.etree.ElementTree as ET

# Set up some variables
CONSUMER_KEY = 'LAe3blOt1IpgcJuJpqGzQ'
#MY_USER_ID = '2686518'

def FindBookID(query):
	# Get an xml file with the most popular books for the given query.
	# This will search all books in the title/author/ISBN fields and
	# show matches, sorted by popularity on Goodreads.
	
	url_base = "http://www.goodreads.com/search.xml"
	params = {'key':CONSUMER_KEY, 'q':query}
	#if shelf is not None: params['shelf'] = 'to-read'
	encoded_params = urllib.urlencode(params)
	url = url_base + '?' + encoded_params
	response = urllib2.urlopen(url)
	search_result = response.read()

	# Print XML content to file
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
			
	# Print the books to the screen
	#for key, value in search_result_dict.iteritems():
		#print key, value[0]
	return search_result_dict.values()[0][2]
	#return search_result_dict.keys()[0]


def BookDescCover(book_id):
	# Get an xml file with the most popular books for the given query.
	# This will search all books in the title/author/ISBN fields and
	# show matches, sorted by popularity on Goodreads.
	
	url_base = "https://www.goodreads.com/book/show/"
	params = {'id':book_id, 'key':CONSUMER_KEY, 'format':'json'}
	encoded_params = urllib.urlencode(params)
	url = url_base + '?' + encoded_params
	response = urllib2.urlopen(url)
	search_result = response.read()
	print search_result
	# Print XML content to file
	#xmlfile = 'book_desc_coverurl.xml'
	#f = open(xmlfile, 'w')
	#f.write(search_result)
	#f.close()

	# Set up the element tree from the XML file
	#tree = ET.parse(xmlfile)
	#root = tree.getroot()

	# Build a list of names based on the <name> tag in the xml file
	#search_result_dict = {}
	#for data in root.find('book'):
	#	book_id = data.find('id').text
	#	book_image_url = data.find('image_url').text
	#	book_title = data.find('title').text
	#	book_desc = data.find('description').text
	#	search_result_dict[book_id] = (book_image_url, book_desc, book_title)
			
	# Print the books to the screen
	#print search_result_dict
	#print search_result_dict.keys()[0]
	#print search_result_dict.values()[0]
	#for key, value in search_result_dict.iteritems():
		#print key, value[0], value[1]
	#return search_result_dict.keys()[0]


def main():
	try:
		print FindBookID(sys.argv[1])
		#print leet.toLeet(bible.doPassageQuery(sys.argv[1]))
		exit(1)
	except IndexError:
		exit(1)
	#query = raw_input('\nEnter the search string: ')
	#print book_image_url
	#BookDescCover(book_id)
	
if __name__ == '__main__':
    main()
