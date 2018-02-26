#!/bin/sh
#
# booktoblog.sh is a bash utility to download the ascii version of a book
# and find haikus in it using the findhaikus program.
# The script takes a file as an argument, with book ids in it on each line.
# Then blog the result to a Blogger blog. 
#
# For example:
# $ ./booktoblog.sh filename.txt
#
# Written by Orjan Vollestad, 2014 orjan@hoyd.net

_file="$1"
[ $# -eq 0 ] && { echo "Usage: $0 filename"; exit 1; }
[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }

if [ -s "$_file" ]
then
	# Get this weeks book id from file and then the url for the text file
	#_id=$(head -1 $_file)
    _id=$(sed -n ''$(date +%V)'p' $_file)
	url=$(python plain-text-url.py $_id)
    
	# download the book
	sleep 15 && wget -O book $url

	# setting some variables
	#EBOOKID=$(grep "eBook #" book | sed 's/.*eBook #//' | sed 's/]//' | strings)
	AUTHOR=$(grep "Author:" book | sed 's/Author: //g' | strings)
	TITLE=$(grep "Title:" book | sed 's/Title: //g' | strings)
	FOLDER=$(echo $TITLE-by-$AUTHOR | sed 's/ /_/g')

	# Get metadata from google books, using a python script
	sleep 15 && python getmetadata.py "$TITLE by $AUTHOR" > temp
	head -1 temp > thumbnail
    
    # if thumbnail from google books didn't work out, use gutenbergs one
	if grep -q xxx thumbnail; then
		echo "http://www.gutenberg.org/cache/epub/$_id/pg$_id.cover.medium.jpg" > thumbnail
	fi
	sed -n '2p' < temp > categories
	sed -n '3p' < temp > pagecount
	sed -n '4,$p' < temp > description

	# run it through findhaikus program and the the haikus in html
	./findhaiku2html.py book > haikus
	sleep 15 && killall findhaikus > /dev/null 2>&1 & 

	# if any haikus found, blog it. If not, do nothing.
	if [ -s haikus ]
	then    
		# replace () in haikus file with empty lines
 		sed -i 's/()//g' haikus

		# insert image into blogentry
		echo "<img src='$(cat thumbnail)' align='right'><p>From a book categorized as $(cat categories) and $(cat pagecount) pages follows a description and a number of hidden haikus found in the book:</p><p><i>$(cat description)</i></p><ul><li>Download the epub for free <a href='http://www.gutenberg.org/ebooks/$_id.epub.noimages'>here</a></li><li>Download the book in raw text for free <a href='$url'>here</a></li></ul>" | cat - haikus > temp && mv temp haikus

		# blog the haikus to blogger
		sleep 15 && python blogger.py --labels "haiku" --title "Haikus from $TITLE by $AUTHOR" --src haikus
	else
		echo "no haikus found"
		# Create folder for book and move away all files
		rm book haikus thumbnail categories pagecount description
		exit 1
	fi
	# Create folder for book and move away all files
	mkdir $FOLDER
	mv -t $FOLDER book haikus thumbnail categories pagecount description
	exit 1
else
	echo "$_file is empty."
	exit 1
fi
