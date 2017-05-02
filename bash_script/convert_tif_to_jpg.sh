#!/usr/bin/env bash


# change the input and output if necessary
arg1=$1
echo $arg1
input=${arg1}
cp ${input} ${input}.backup

output=tif_jpg.txt
#rm ${output}

while IFS= read -r line
do
#show the line
#echo $line

#save tif file and png file to oupput
strings=($line)
tif_file=${strings[0]}
png_file=${strings[1]}
jpg_file=${tif_file::-4}.jpg
#echo ${tif_file} ${jpg_file} ${png_file}

#exit
gdal_translate -of JPEG ${tif_file} ${jpg_file}

echo ${jpg_file} ${png_file} >> ${output}

done < "$input"

mv ${output} ${input}

