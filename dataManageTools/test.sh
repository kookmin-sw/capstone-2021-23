#!bin/bash

DIR_LIST="
test_kicking
test_normal
test_punching
"

for dir in $DIR_LIST
do
	echo $dir
	for file in $dir/*
	do
		python test.py $file

	done
done
