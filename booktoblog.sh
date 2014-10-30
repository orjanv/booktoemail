#!/bin/sh
#
# booktoblog.sh is a bash utility to download the ascii version of a book
# and find haikus in it using the findhaikus program.
# The script takes a file as an argument, with book ids in it on each line.
# Then by using googlecl, blog the result to a Blogger blog. 
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
	# Get the top book id
	_id=$(head -1 $_file)

	# download the book based on the book ID number given as args, for ex: 2591
	wget -O book http://www.gutenberg.org/files/$_id/$_id.txt

	# setting some variables
	AUTHOR=$(grep "Author:" book | sed 's/Author: //g' | strings)
	TITLE=$(grep "Title:" book | sed 's/Title: //g' | strings)
	echo $TITLE
	FOLDER=$(echo $TITLE-by-$AUTHOR | sed 's/ /_/g')

	# find cover from google books, using a python script
	python getthumbdesc.py $TITLE $AUTHOR > thumb_desc
	head -1 thumb_desc > image_url
	sed -n '2,$p' <thumb_desc > description
	rm thumb_desc

	# run it through findhaikus program
	/usr/local/bin/findhaikus book > haikus
	sleep 15 && killall findhaikus > /dev/null 2>&1 & 

	# if any haikus found, blog it. If not, do nothing.
	if [ -s haikus ]
	then    
		# replace () in haikus file with empty lines
 		sed -i 's/()//g' haikus

		# insert image into blogentry
		echo "<img src='$(cat image_url)' align='right'><p><b>About the book:</b></p><p>$(cat description)</p>" | cat - haikus > temp && mv temp haikus

		# blog the haikus to blogger
		google blogger post --tags "haiku" --title "Haikus from $TITLE by $AUTHOR" --src haikus
		echo "posted on blogger"
	else
		echo "no haikus found"
		# remove book id from file, create folder for book and move away all files
		mkdir $FOLDER
		mv -t $FOLDER book haikus image_url
		sed -i '1d' $_file
		# run the script again if no haikus found
		booktoblog.sh $_file 
		exit 1
	fi
	# remove book id from file, create folder for book and move away all files
	mkdir $FOLDER
	mv -t $FOLDER book haikus image_url description
	sed -i '1d' $_file
	exit 1
else
	echo "$_file is empty."
	exit 1
fi

