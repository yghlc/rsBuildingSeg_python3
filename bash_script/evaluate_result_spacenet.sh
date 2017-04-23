#!/usr/bin/env bash

#truecsv=$1
#detectedcsv=$2

spacenet_root=${HOME}/Data/aws_SpaceNet/un_gz
output_root=${HOME}/Data/aws_SpaceNet/deeplab_exper

exprid=spacenet_rgb_aoi_3
network=deeplab_largeFOV

python_script=${HOME}/codes/PycharmProjects/rsBuildingSeg/SpaceNetChallenge/utilities/python/evaluateScene.py

truecsv=${spacenet_root}/AOI_3_Paris_Train/summaryData/AOI_3_Paris_Train_Building_Solutions.csv
detectedcsv=${output_root}/${exprid}/features/${network}/val/fc8/result_buildings.csv

echo SpaceNetTruthFile: ${truecsv}
echo SpaceNetProposalFile: ${detectedcsv}

# for my first test, --useParallelProcessing make the F1 score to be 0
python ${python_script} ${truecsv} ${detectedcsv} --resultsOutputFile SpaceNetResults.csv