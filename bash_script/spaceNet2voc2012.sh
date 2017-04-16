#!/bin/bash

spacenet_root=${HOME}/Data/aws_SpaceNet/un_gz
output_root=${HOME}/Data/aws_SpaceNet/voc_format
python_script=${HOME}/codes/PycharmProjects/rsBuildingSeg/SpaceNetChallenge/utilities/python/createDataSpaceNet.py

#${spacenet_root}
AOI_2=AOI_2_Vegas_Train
AOI_3=AOI_3_Paris_Train
AOI_4=AOI_4_Shanghai_Train
AOI_5=AOI_5_Khartoum_Train


#echo ${AOIs} ${AOI_3} ${AOI_4} ${AOI_5}
for AOI in ${AOI_2} ${AOI_3} ${AOI_4} ${AOI_5}
do
    echo training data dir: $spacenet_root/$AOI

    #using createDataSpaceNet.py to convert spaceNet file to PASCALVOC2012 format
#    python python/createDataSpaceNet.py /path/to/spacenet_sample/AOI_2_Vegas_Train/ \
#           --srcImageryDirectory RGB-PanSharpen
#           --outputDirectory /path/to/spacenet_sample/annotations/ \
#           --annotationType PASCALVOC2012 \
#           --imgSizePix 400

    #using createDataSpaceNet.py to convert spaceNet file to PASCALVOC2012 format
    python ${python_script} ${spacenet_root}/${AOI} \
           --srcImageryDirectory RGB-PanSharpen
           --outputDirectory ${output_root}/${AOI}/annotations/ \
           --annotationType PASCALVOC2012 \
           --imgSizePix 400
done

#echo $AOI_2
exit

