#!/usr/bin/env python
import json, requests, sys, os

# Set to 1 to print out the json in pretty format, for debugging
#~ DEBUG = '1'

def GoogleBooks(query, _author):
	user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
	results = requests.get("https://www.googleapis.com/books/v1/volumes", 
		params={'q': query, 
				'inauthor': _author,
				#~ 'maxResults':'3',
				'printType':'books',
				'full':'full'},
		headers={'User-Agent': user_agent})
	data = results.json()

	# set some default values
	thumbnail = 'http://s.gr-assets.com/assets/nophoto/book/111x148-c93ac9cca649f584bf7c2539d88327a8.png'
	description = ''
	categories = ''
	pagecount = ''
	selflink = ''
	newdata = ''

	file = open('pretty.json','w+')
	file.write(json.dumps(data, sort_keys=True, indent=4))
	file.close()

	# find where volumeInfo > authors matches _author
	# loop through the items in the first json
	for book in data['items']:
		if book[u'volumeInfo'][u'authors'][0] == _author:
			user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
			results = requests.get(book.get('selfLink'), headers={'User-Agent': user_agent})
			newdata = results.json()
			
			file = open('pretty-new.json','w+')
			file.write(json.dumps(newdata, sort_keys=True, indent=4))
			file.close()
			
			try:
				thumbnail = newdata[u'volumeInfo'][u'imageLinks'][u'thumbnail']
			except KeyError: pass
			try:
				description = newdata[u'volumeInfo'][u'description']
			except KeyError: pass
			try:
				categories = newdata[u'volumeInfo'][u'categories'][0]
			except KeyError: pass
			try:
				pagecount = newdata[u'volumeInfo'][u'pageCount']
			except KeyError: pass
			
			print thumbnail
			print categories.encode('utf-8')
			print pagecount
			print description.encode('utf-8')

			break

def main():
	try:
		GoogleBooks(sys.argv[1], sys.argv[2])
		exit(1)
	except IndexError:
		exit(1)
	
if __name__ == '__main__':
    main()
