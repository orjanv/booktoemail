#!/bin/sh
#
# booktoblog.sh is a bash utility to download the ascii version of a book
# and find haikus in it using the findhaikus program.
# The script takes a file as an argument, with book ids in it on each line
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
    echo "$_file has some data."

    # Get the top book id and remove it from the list
    _id=$(head -1 $_file)
    sed -i '1d' $_file

    # download the book based on the book ID number given as args, for ex: 2591
    wget -O book http://www.gutenberg.org/files/$_id/$_id.txt

    # setting some variables
    AUTHOR=$(grep "Author:" book | sed 's/Author: //g' | strings)
    TITLE=$(grep "Title:" book | sed 's/Title: //g' | strings)

    FOLDER=$(echo $TITLE-by-$AUTHOR | sed 's/ /_/g')

    # run it through findhaikus program
    findhaikus book > haikus

    # replace () in haikus file with empty lines
    sed -i 's/()//g' haikus

    # blog the haikus to blogger
    google blogger post --tags "haiku" --title "Haikus from $TITLE by $AUTHOR" --src haikus

    # create folder for book and move away all files
    mkdir $FOLDER
    mv -t $FOLDER book haikus

else
    echo "$_file is empty."
    exit 1
fi

