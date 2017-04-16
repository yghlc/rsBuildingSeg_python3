#!/usr/bin/env bash

# put this file to ${training_data_root} and run test

spacenet_root=${HOME}/Data/aws_SpaceNet/un_gz
output_root=${HOME}/Data/aws_SpaceNet/voc_format
python_script=${HOME}/codes/PycharmProjects/rsBuildingSeg/SpaceNetChallenge/utilities/python/createDataSpaceNet.py

#${spacenet_root}
AOI_2=AOI_2_Vegas_Train
AOI_3=AOI_3_Paris_Train
AOI_4=AOI_4_Shanghai_Train
AOI_5=AOI_5_Khartoum_Train

AOI=${AOI_2}

#./remove_training_data.sh

COUNTER=0
while [ $COUNTER -lt 10 ]
do

#python /home/hlc/codes/PycharmProjects/rsBuildingSeg/SpaceNetChallenge/utilities/python/createDataSpaceNet.py \
#${AOI_root} --srcImageryDirectory RGB-PanSharpen \
#--outputDirectory /home/hlc/Data/aws_SpaceNet/voc_format/AOI_2_Vegas_Train/ \
#--annotationType PASCALVOC2012 --spacenetVersion 2

training_data_root=${spacenet_root}/${AOI}
outputDirectory=${output_root}/${AOI}/

#using createDataSpaceNet.py to convert spaceNet file to PASCALVOC2012 format
python ${python_script} ${training_data_root} --srcImageryDirectory RGB-PanSharpen --outputDirectory ${outputDirectory} --annotationType PASCALVOC2012

echo '*******************PYTHON SCRIPT IS CRASHED, RESTART*****************************************'
sleep 2

./remove_training_data.sh

let COUNTER=COUNTER+1

done
