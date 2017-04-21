#!/bin/bash


infoLog=$1
savepng=$2

echo input log file is: $infoLog
echo saving png file is: $savepng

#infoLog=/Users/huanglingcao/codes/PycharmProjects/rsBuildingSeg/caffe.bin.Cryo06.hlc.log.INFO.20170419-181307.6896

home_dir=($HOME)
codes_dir=$home_dir/codes/PycharmProjects/rsBuildingSeg
draw_script=($codes_dir/DeepLab-Context/tools/extra/plot_training_log.py.example)

echo draw_script: ${draw_script}


#Notes:
#    1. Supporting multiple logs.
#    2. Log file name must end with the lower-cased ".log".
#Supported chart types:
#    0: Test accuracy  vs. Iters
#    1: Test accuracy  vs. Seconds
#    2: Test loss  vs. Iters
#    3: Test loss  vs. Seconds
#    4: Train learning rate  vs. Iters
#    5: Train learning rate  vs. Seconds
#    6: Train loss  vs. Iters
#    7: Train loss  vs. Seconds
#draw Train loss  vs. Iters
python ${draw_script} 6 ${savepng} ${infoLog}