#!/usr/bin/env bash

# aoi 2, aoi 3 run on GPU 0, need manually set on the python script

# run in the exper dir, eg, ~/Data/aws_SpaceNet/deeplab_exper

cd spacenet_rgb_aoi_2

./run_train.py
./run_test_and_evaluate.py
./evaluate_result_spacenet.sh

cd ..



cd spacenet_rgb_aoi_3

./run_train.py
./run_test_and_evaluate.py
./evaluate_result_spacenet.sh

cd ..

