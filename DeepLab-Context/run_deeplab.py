#!/usr/bin/env python
# Filename: run_deeplab 
"""
introduction: processing the remote sensing data by using deeplab frame, modify from DeepLab-Context/run.py

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 17 April, 2017
"""

import os, sys, subprocess
from optparse import OptionParser

# import model from DeepLab-Context/python/my_script/
sys.path.insert(0, os.getcwd() + '/python/my_script/')
from tester import tester
from trainer import trainer
from crf_runner import crf_runner, grid_search
import tools

# MODIFY PATH for YOUR SETTING
# EXP = '/home/hlc/Data/deeplab/exper/voc12'  # dataset
EXP='/home/hlc/Data/aws_SpaceNet/deeplab_exper/spacenet_rgb_aoi_2'
# NET_ID='vgg128_noup' #model name
NET_ID = 'deeplab_largeFOV'  # model name
# NET_ID='DEEPLAB_ICLR2015paper'
# NUM_LABELS = 21
NUM_LABELS = 2
YEAR = '2017'
# DATA_ROOT = '/home/hlc/Data/aws_SpaceNet/voc_format/AOI_2_Vegas_Train'
DATA_ROOT = ''  # the data file store in text file already use absolute path
# DATA_ROOT=subprocess.Popen('cd .. && pwd', stdout=subprocess.PIPE, shell=True).communicate()[0][:-1] + '/VOCdevkit/' + YEAR
OLD_ROOT = ''  # only change if you are changing the path to images
DEV_ID = 0  # gpu id
LOAD_MAT_FILE = 1

train_set_SUFFIX = '_aug'

train_set_STRONG = 'train'
# train_set_STRONG='train200'
# train_set_STRONG='train500'
# train_set_STRONG='train1000'
# train_set_STRONG='train750'

train_set_WEAK_LEN = 0  # '5000'

# Run

RUN_TRAIN = 0  # Training #1 (on train_aug)
RUN_TEST = 0  # Test #1 specification (on val or test)
RUN_TRAIN2 = 0  # Training #2 (finetune on trainval_aug)
RUN_TEST2 = 1  # Test #2 on official test set
RUN_SAVE = 0  # Translate and save the model
RUN_DENSECRF = 0  # To Run Densecrf
GRID_SEARCH = 0  # To Run ONLY if you dont know what parameters to use for Densecrf

#####

def env_creater():
    dic = {'EXP': EXP, 'NET_ID': NET_ID, 'NUM_LABELS': NUM_LABELS, 'DATA_ROOT': DATA_ROOT, 'DEV_ID': DEV_ID,
           'OLD_ROOT': OLD_ROOT}
    dic.update({'train_set_SUFFIX': train_set_SUFFIX, 'train_set_STRONG': train_set_STRONG,
                'train_set_WEAK_LEN': train_set_WEAK_LEN})
    dic.update({'year': YEAR, 'POSTPROCESS': 0})
    tools.environment_variable_creator(dic)


def run(RUN_TRAIN, RUN_TEST, RUN_TRAIN2, RUN_TEST2, RUN_SAVE):
    tools.mkdir()
    if RUN_TRAIN: trainer()
    if RUN_TEST: tester()
    if RUN_TRAIN2: trainer(type_=2)
    if RUN_TEST2: tester(type_=2)
    if RUN_SAVE: tools.saver()
    if RUN_DENSECRF: crf_runner(LOAD_MAT_FILE, RUN_TRAIN2)
    if GRID_SEARCH: grid_search(LOAD_MAT_FILE, RUN_TRAIN2)


def main(options, args):

    env_creater()
    run(RUN_TRAIN, RUN_TEST, RUN_TRAIN2, RUN_TEST2, RUN_SAVE)

    pass



if __name__=='__main__':
    usage = "usage: %prog [options] geojson_folder  backup_folder"
    parser = OptionParser(usage=usage, version="1.0 2017-4-17")
    (options, args) = parser.parse_args()

    main(options, args)

