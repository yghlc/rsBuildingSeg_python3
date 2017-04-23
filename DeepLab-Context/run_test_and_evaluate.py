#!/usr/bin/env python
# Filename: run_test_and_evaluate.py
"""
introduction: run the test by using run_deeplab.py, convert the result in Mat by using matlab script
                convert the result to csv table and evaluate the result

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 22 April, 2017
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
import subprocess,numpy

from PIL import Image

import basic.basic as basic
import basic.io_function as io_function
from basic.RSImage import RSImageclass
from basic.RSImageProcess import RSImgProclass
import basic.mat_To_png as mat_To_png

# sys.path.insert(0, codes_path + '/SpaceNetData')
import SpaceNetData.geoJSONfromCluster as geoJSONfromCluster
import SpaceNetData.FixGeoJSON as FixGeoJSON

#sys.path.insert(0, os.getcwd() + '../SpaceNetChallenge/')
import SpaceNetChallenge.utilities.python.createCSVFromGEOJSON as createCSVFromGEOJSON


if os.path.isdir(expr) is False:
    print 'error, % not exist '%expr
    exit(1)

run_deeplab.EXP = expr
run_deeplab.DEV_ID = gpuid
run_deeplab.NET_ID = NET_ID

test_file = expr+'/list/val.txt'
# id is need in caffe for output result
test_file_id = expr+'/list/val_id.txt'

# need to change the mean value and cropsize
test_prototxt_tem = os.path.join(expr,'config',NET_ID,'test.prototxt')

mat_file_foler = expr+'/features/'+NET_ID+ '/val/fc8'




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


def run_test():
    run_deeplab.RUN_TEST = 1
    # set other to be zeros
    run_deeplab.RUN_TRAIN = 0
    run_deeplab.RUN_TRAIN2 = 0
    run_deeplab.RUN_TEST2 = 0
    run_deeplab.RUN_SAVE = 0
    run_deeplab.RUN_DENSECRF = 0
    run_deeplab.GRID_SEARCH = 0

    run_deeplab.main(None,None)

    pass

def convert_mat_to_png(mat_folder, b_runmatlab=True):

    # need to run matlab script
    # original_path = str(os.getcwd())
    # path = os.path.join(codes_path,'DeepLab-Context','matlab','my_script')
    # os.chdir(path)
    # # convert the mat files to png or tif
    # if b_runmatlab :
    #     subprocess.call("matlab -r 'converttoPng; exit;'", shell=True)
    # os.chdir(original_path)

    # using python script instead of matlab script
    if mat_To_png.convert_mat_to_png(mat_folder) is False:
        return False

    # read the png or tif files list
    result = io_function.get_file_list_by_ext('.tif',mat_file_foler,bsub_folder=False)
    if len(result) < 1:
        result = io_function.get_file_list_by_ext('.png', mat_file_foler, bsub_folder=False)
    if len(result) < 1:
        basic.outputlogMessage('error, Not result (.tif or .png) in Mat folder:%s'%mat_file_foler)
        return False
    if len(result) != len(test_data):
        basic.outputlogMessage('error, the count of results is not the same as input test file')
        return False
    return result

def convert_png_result_to_geojson(result_list):
    rsimg_obj = RSImageclass()
    rsimgPro_obj = RSImgProclass()

    if len(result_list) != len(test_data):
        basic.outputlogMessage('error, the count of results is not the same as input test file')
        return False

    geojson_without_fix_folder = os.path.join(mat_file_foler,'geojson_without_fix')
    io_function.mkdir(geojson_without_fix_folder)

    geojson_folder = os.path.join(mat_file_foler,'geojson')
    io_function.mkdir(geojson_folder)

    basic.outputlogMessage('geojson_without_fix_folder: %s'%geojson_without_fix_folder)
    basic.outputlogMessage('geojson_folder: %s'%geojson_folder)


    geojson_list = []

    for i in range(0,len(result_list)):
        # read geo information
        if rsimg_obj.open(test_data[i][0]) is False:
            return False
        result_file = os.path.join( os.path.split(result_list[i])[0] , test_data[i][2]+'_blob_0.png')
        if result_file not in result_list:
            basic.outputlogMessage('result_file file not in the list %s'%result_file)
            return False
        basic.outputlogMessage('png to geojson: %d / %d :Convert file: %s'%(i+1, len(result_list),os.path.basename(result_file)))

        prj = rsimg_obj.GetProjection()
        geom = rsimg_obj.GetGeoTransform()

        # read pixel value
        im_data = rsimgPro_obj.Read_Image_band_data_to_numpy_array_all_pixel(1,result_file)
        if im_data is False:
            basic.outputlogMessage('Read image data failed: %s'%result_file)
            return False
        # im = Image.open(result_file)  # Can be many different formats.
        # pix = im.load()
        # im_data = numpy.array(pix)

        imgID = test_data[i][2]

        geojson = geoJSONfromCluster.CreateGeoJSON(geojson_without_fix_folder,imgID,im_data,geom,prj)
        fix_geojson = FixGeoJSON.FixGeoJSON(geojson,geojson_folder)
        geojson_list.append(fix_geojson)

    return geojson_list


def spaceNet_evaluate():
    pass


def main():

    if read_test_data(test_file,test_file_id) is False:
        return False

    run_test()

    # get the deeplab output result, in png or tif format
    # result_list = convert_mat_to_png()
    result_list = convert_mat_to_png(mat_file_foler,b_runmatlab=True)
    if result_list is False:
        return False

    # the file in result_list don't have the same order as the files in read_data

    #convert the result to csv table
    geojson_list = convert_png_result_to_geojson(result_list)

    # original raster file list, can get extract imageID
    rasterList = [item[0] for item in test_data]
    outputCSVFileName = os.path.join(mat_file_foler,'result_buildings.csv')
    if createCSVFromGEOJSON.createCSVFromGEOJSON(rasterList,geojson_list,outputCSVFileName) is not True:
        return False

    # evaluate
    # use a separate bash file to do evaluate

    pass

if __name__=='__main__':
    main()