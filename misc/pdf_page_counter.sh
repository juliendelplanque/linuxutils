#!/bin/bash

# Little script to compute the sum of the number of pages of all pdf files
# in the directory $DIR and from this, compute the price of an impression of
# these files according to the price per page $PRICE.
# 
# This a fast-coded script, you can modify/improve it as you want.
#
# Dependency: pdfinfo
#
# Author: Julien Delplanque
# Date: 26/09/2014

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

DIR="."      # This will execute the script on the current dir.
PRICE="0.02" # This is the price of one impression, you may want to modify it.

sum=0
for file in $(ls $DIR)
do
    if [[ $file == *".pdf" ]]
    then
        pages=$(pdfinfo -meta $file | sed -n -e "s/^Pages:[[:space:]]*\([0-9]*\)/\1/p")
        echo "$file: $pages page(s)"
        let "sum += pages"
    fi
done

echo "-------------------"
echo "Total: $sum page(s)"
echo "Price: $(bc <<< $PRICE"*$sum")"

IFS=$SAVEIFS

exit 0