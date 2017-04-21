#!/usr/bin/env bash

#!/usr/bin/env bash

# this file run at folder like: voc_format/AOI_2_Vegas_Train

# change the input and output if necessary
arg1=$1
echo $arg1
input=${arg1}.txt
output=${arg1}_aug.txt

echo $input
echo $output

rm ${output}

while IFS= read -r line
do
#show the line
echo $line
#get image id
substr=(${line:(-10)})
imgid=$(tr -dc '0-9' <<<  $substr)
echo $imgid

#find segobj file. In segobj file, the pixel of each building was burned to different value
#cd annotations
#newfile=$(pwd)/$(ls *img${imgid}segobj.png)
#echo $newfile
#cd ..

#find segcls file. In segcls file, the pixel of each building was burned to 100
cd annotations
newfile=$(pwd)/$(ls *img${imgid}segcls.png)
echo $newfile
cd ..

#save tif file and png file to oupput
tif=($line)
echo ${tif[0]} $newfile >>${output}

done < "$input"