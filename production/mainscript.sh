#!/bin/bash

# Ask the user for their name
echo Welcome to DDM-util. 
echo This is a utility to analyze images obtained by DDM!
while true
do
	read -p "Do you want to analyze images? Enter y for yes and n for no." yn
	echo 
	if [ varname == "y" ]
	then
		echo "Entered Yes"
	else
		echo "Entered No"
	fi
done
# read varname
# if [ varname ]