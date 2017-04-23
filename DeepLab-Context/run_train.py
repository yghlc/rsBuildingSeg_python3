#!/usr/bin/env python
# Filename: run_train.py
"""
introduction: run the train by using run_deeplab.py

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 23 April, 2017
"""

import os,sys
# modify this if necessary
codes_path = '/home/hlc/codes/PycharmProjects/rsBuildingSeg'
sys.path.insert(0, codes_path)

# modify this if necessary
expr='/media/hlc/DATA/Data_lingcao/aws_SpaceNet/deeplab_exper/spacenet_rgb_aoi_2'
gpuid = 0
NET_ID = 'deeplab_largeFOV'  # model name


sys.path.insert(0, codes_path+'/DeepLab-Context')
sys.path.insert(0,codes_path+'/DeepLab-Context/python/my_script/')

os.environ['DEEPLAB'] = codes_path+'/DeepLab-Context'
print os.environ['DEEPLAB']
import run_deeplab

import basic.basic as basic
import basic.io_function as io_function
from basic.RSImage import RSImageclass
from basic.RSImageProcess import RSImgProclass


if os.path.isdir(expr) is False:
    print 'error, % not exist '%expr
    exit(1)

run_deeplab.EXP = expr
run_deeplab.DEV_ID = gpuid
run_deeplab.NET_ID = NET_ID

#TRAIN = 1
train_file = os.path.join(expr,'/list/train_aug.txt')
test_file = os.path.join(expr,'/list/train_aug.txt')
train_prototxt_tem = os.path.join(expr,'config',NET_ID,'train.prototxt')
train_solver_tem = os.path.join(expr,'config',NET_ID,'solver.prototxt')


test_data = []

def read_test_data(test_file,file_id):
    if os.path.isfile(test_file) is False:
        basic.outputlogMessage('error: file not exist %s'%test_file)
        return False
    f_obj = open(test_file)
    fid_obj = open(file_id)
    f_lines = f_obj.readlines()
    fid_lines = fid_obj.readlines()
    fid_obj.close()
    f_obj.close()

    if len(f_lines) != len(fid_lines):
        basic.outputlogMessage('the number of lines in test_file and test_file_id is not the same')
        return False

    for i in range(0,len(f_lines)):
        temp = f_lines[i].split()
        # temp[1].
        temp.append(fid_lines[i].strip())
        test_data.append(temp)

    return True


def run_train():
    # train 1
    run_deeplab.RUN_TEST = 0
    # set other to be zeros
    run_deeplab.RUN_TRAIN = 1
    run_deeplab.RUN_TRAIN2 = 0
    run_deeplab.RUN_TEST2 = 0
    run_deeplab.RUN_SAVE = 0
    run_deeplab.RUN_DENSECRF = 0
    run_deeplab.GRID_SEARCH = 0

    run_deeplab.main(None,None)

    pass


def main():



    pass

if __name__=='__main__':
    main()