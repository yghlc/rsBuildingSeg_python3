#!/usr/bin/env bash

truecsv=$1
detectedcsv=$2

spacenet_root=${HOME}/Data/aws_SpaceNet/un_gz
output_root=${HOME}/Data/aws_SpaceNet/voc_format

python_script=${HOME}/codes/PycharmProjects/rsBuildingSeg/SpaceNetChallenge/utilities/python/evaluateScene.py

truecsv=${spacenet_root}/AOI_2_Vegas_Train/summaryData/AOI_2_Vegas_Train_Building_Solutions.csv

echo SpaceNetTruthFile: ${truecsv}
echo SpaceNetProposalFile: ${detectedcsv}

# for my first test, --useParallelProcessing make the F1 score to be 0
python ${python_script} ${truecsv} ${detectedcsv} --resultsOutputFile SpaceNetResults.csv