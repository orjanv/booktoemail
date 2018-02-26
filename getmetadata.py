#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import sys

# Set to 1 to print out the json in pretty format, for debugging
DEBUG = '0'


def GoogleBooks(query):
    user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
    results = requests.get("https://www.googleapis.com/books/v1/volumes",
                           params={'q': query,
                                   'printType': 'books',
                                   'full': 'full'},
                           headers={'User-Agent': user_agent})
    data = results.json()

    # set some default values
    thumbnail = 'xxx'
    description = ''
    categories = ''
    pagecount = ''
    selflink = ''
    newdata = ''

    if DEBUG == '1':
        file = open('pretty.json', 'w+')
        file.write(json.dumps(data, sort_keys=True, indent=4))
        file.close()

    # find where volumeInfo > authors matches _author
    # loop through the items in the first json
    for book in data['items']:
		user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
		results = requests.get(book.get('selfLink'), headers={'User-Agent': user_agent})
		newdata = results.json()

		if DEBUG == '1':
			file = open('pretty-new.json', 'w+')
			file.write(json.dumps(newdata, sort_keys=True, indent=4))
			file.close()

		try:
			thumbnail = newdata[u'volumeInfo'][u'imageLinks'][u'thumbnail']
		except KeyError:
			pass
		try:
			description = newdata[u'volumeInfo'][u'description']
		except KeyError:
			pass
		try:
			categories = newdata[u'volumeInfo'][u'categories'][0]
		except KeyError:
			pass
		try:
			pagecount = newdata[u'volumeInfo'][u'pageCount']
		except KeyError:
			pass

		print thumbnail
		print categories.encode('utf-8')
		print pagecount
		print description.encode('utf-8')

		break


def main():
    try:
        GoogleBooks(sys.argv[1])
        exit(1)
    except IndexError:
        exit(1)


if __name__ == '__main__':
    main()
