#!/usr/bin/env python
import json, requests, sys, os

def GoogleBooks(_title, _author):
	user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
	results = requests.get("https://www.googleapis.com/books/v1/volumes", 
		params={'q': _title, 
				'inauthor': _author,
				'maxResults':'1',
				'printType':'books',
				'full':'full'},
		headers={'User-Agent': user_agent})
	data = results.json()
	
	thumbnail = data["items"][0][u'volumeInfo'][u'imageLinks'][u'thumbnail']
	try:
		description = data["items"][0][u'volumeInfo'][u'description']
	except KeyError: pass

	print thumbnail
	print description.encode('utf-8')

	file = open('pretty.json','w+')
	file.write(json.dumps(data, sort_keys=True, indent=4))
	file.close()

def main():
	try:
		GoogleBooks(sys.argv[1], sys.argv[2])
		exit(1)
	except IndexError:
		exit(1)
	
if __name__ == '__main__':
    main()
