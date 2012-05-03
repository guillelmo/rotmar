#!/bin/bash

while getopts "p:t:b:" optname
do
    case "$optname" in
	"p")
	    p=$OPTARG
	    ;;
	"t")
	    t=$OPTARG
	    ;;
	"b")
	    b=$OPTARG
	    ;;
    esac    
done

if [ -z "$b" ] || [ -z "$t" ]
then
    echo "Error: The range is not correctly set."
    echo "Ex: ./script.sh -b 1 -t 8240 "
    exit 0
fi

let bottom=($b / 1000)
let top=($t / 1000)

for i in `seq $bottom $top`
do
    let NAME=($i*1000)
    mkdir "$p$NAME"
done

cat /dev/null > found.txt
cat /dev/null > notfound.txt

