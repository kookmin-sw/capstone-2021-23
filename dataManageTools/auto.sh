#!bin/bash

for file in ./*mp4
do
	a=$file 
	b=$(cut -d'.' -f2 <<<$a)
	c=$(cut -d'/' -f2 <<<$b)
	#echo $c
	python3 parser.py --name $c
done
