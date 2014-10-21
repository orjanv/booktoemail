#!/bin/sh
# 
# booktoemail.sh is a bash utility to download the ascii version of a book
# and find haikus in it using the findhaikus program. The script takes 2 arguments
#
# $ booktoemail.sh URL EMAIL_ADDRESS
# 
# For example:
# $ ./booktoemail.sh http://www.gutenberg.org/files/2591/2591.txt orjan@hoyd.net
# 
# Written by Orjan Vollestad, 2014 orjan@hoyd.net

# download the book
wget -O book $1

# setting some variables
AUTHOR=$(grep "Author:" book | sed 's/Author: //g')
TITLE=$(grep "Title:" book | sed 's/Title: //g' | 's/^M//g')

FOLDER=$(echo $TITLE | sed 's/ /_/g')

# run it through findhaikus program
findhaikus book > haikus

# replace () in haikus file with empty lines
sed -i 's/()//g' haikus

# send the content by email
cat haikus | mailx -s "$TITLE by $AUTHOR" $2

# create folder for book and move away all files
mkdir $FOLDER
mv -t $FOLDER book haikus
