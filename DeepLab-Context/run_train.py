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
import basic.calculate_meanvalue as calculate_meanvalue
from basic.RSImage import RSImageclass
from basic.RSImageProcess import RSImgProclass


if os.path.isdir(expr) is False:
    print 'error, % not exist '%expr
    exit(1)

run_deeplab.EXP = expr
run_deeplab.DEV_ID = gpuid
run_deeplab.NET_ID = NET_ID

#TRAIN = 1
train_file = os.path.join(expr,'list/train_aug.txt')
test_file = os.path.join(expr,'list/test_aug.txt')
train_prototxt_tem = os.path.join(expr,'config',NET_ID,'train.prototxt')
train_solver_tem = os.path.join(expr,'config',NET_ID,'solver.prototxt')
test_prototxt_tem = os.path.join(expr,'config',NET_ID,'test.prototxt')


test_data = []

def cal_mean_value_of_each_band(train_file,test_file):

    if io_function.is_file_exist(train_file) is False or io_function.is_file_exist(test_file) is False:
        return False

    whole_data_set = []
    f_obj = open(train_file,'r')
    for line in f_obj.readlines():
        img_path = line.split()[0]
        whole_data_set.append(img_path)
    f_obj.close()

    f_obj = open(test_file,'r')
    for line in f_obj.readlines():
        img_path = line.split()[0]
        whole_data_set.append(img_path)
    f_obj.close()

    # for i in range(0,len(f_lines)):
    #     temp = f_lines[i].split()
    #     # temp[1].
    #     temp.append(fid_lines[i].strip())
    #     test_data.append(temp)

    mean_of_images = calculate_meanvalue.calculate_mean_of_images(whole_data_set)

    # write means to train_prototxt_tem and test_prototxt_tem
    # set it manually
    f_obj =  open('mean_value.txt','w')
    for i in range(0,len(mean_of_images)):
        f_obj.writelines('band {}: mean {} \n'.format(i+1,mean_of_images[i]))
    f_obj.close()

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
    # need to run and set the mean value manully at first time
    # cal_mean_value_of_each_band(train_file,test_file)

    # make sure alreay prepare the init model, set iteration number .... manully
    run_train()


    pass

if __name__=='__main__':
    main()