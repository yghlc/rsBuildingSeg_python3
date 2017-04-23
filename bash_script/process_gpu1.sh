#!/usr/bin/env bash

# aoi 4, aoi 5 run on GPU 1,  need manually set on the python script

# run in the exper dir, eg, ~/Data/aws_SpaceNet/deeplab_exper

cd spacenet_rgb_aoi_4

./run_train.py
./run_test_and_evaluate.py
./evaluate_result_spacenet.sh

cd ..



cd spacenet_rgb_aoi_5

./run_train.py
./run_test_and_evaluate.py
./evaluate_result_spacenet.sh

cd ..
