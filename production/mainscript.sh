#!/usr/bin/env bash

# Ask the user for their name
echo Welcome to DDM-util. 
echo This is a utility to analyze images obtained by DDM!
while true; do
	read -p "Do you want to analyze images?" yn 
echo Enter y for yes and n for no.
read varname
if [ varname ]