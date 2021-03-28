#!/bin/bash

unzip /home/taehyeon/Desktop/dataset/original/*.zip -d /home/taehyeon/Desktop/dataset/original/
rm /home/taehyeon/Desktop/dataset/original/*.zip

root="/home/taehyeon/Desktop/dataset/original/*"
for dic in $root
do
	for file in $dic/*.mp4
	do
		ffmpeg -i $file -s 960x540 /home/taehyeon/Desktop/dataset/downsize/${file##*/}
	done
	mv $dic/*.xml /home/taehyeon/Desktop/dataset/downsize/
done

rm -rf $root
