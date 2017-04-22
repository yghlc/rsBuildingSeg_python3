#!/usr/bin/env bash


# change the input and output if necessary
arg1=$1
echo $arg1
input=${arg1}.txt
output=${arg1}_id.txt

echo $input
echo $output

rm ${output}

while IFS= read -r line
do
#show the line
echo $line

#save tif file and png file to oupput
tif=($line)
fullfile=${tif[0]}

#get file name without the path
filename=$(basename "$fullfile")

#extension="${filename##*.}"
filename="${filename%.*}"

echo ${filename}  >>${output}
#exit

done < "$input"