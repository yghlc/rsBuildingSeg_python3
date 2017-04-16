#!/usr/bin/env python
# Filename: rmPointLayerinGeojson.py
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 16 April, 2017
"""

# import sys
from optparse import OptionParser
import basic, io_function

def rmPointsinGeojson(path,backup_folder):
    hasPoint = False
    f_obj = open(path,'r')
    # i=0
    save_lines = []
    for line in f_obj.readlines():
        # i = i+1;
        # if i==16:
        #     test = 1
        if line.find('Point') > 0:
            hasPoint = True
            continue
        else:
            save_lines.append(line)

    f_obj.close()

    if hasPoint is True:
        # backup
        io_function.copyfiletodir(file, backup_folder)

        fw_obj = open(path,'w')
        # for line in save_lines:
        fw_obj.writelines(save_lines)
        fw_obj.close()


def process_folder(folder_path,backup_folder):
    folder_path = io_function.get_absolute_path(folder_path)
    backup_folder = io_function.get_absolute_path(backup_folder)
    if folder_path == backup_folder:
        basic.outputlogMessage('backup folder is the same as geojson folder')
        return False

    # create backup folder
    io_function.mkdir(backup_folder)

    basic.outputlogMessage('the folder contains geojson: ' + folder_path)
    basic.outputlogMessage('backup folder: ' + backup_folder)
    #list file
    file_list = io_function.get_file_list_by_ext('.geojson',folder_path,bsub_folder=True)
    if len(file_list) < 0:
        basic.outputlogMessage('error, no geojson found in '+folder_path)
        return False
    for file in file_list:

        # rmPointsinGeojson(path)
        rmPointsinGeojson(file,backup_folder)

    #remove Point in Geojson
    pass


def main(options, args):
    path = "/Users/huanglingcao/Desktop/buildings_AOI_2_Vegas_img1 (copy).geojson"
    folder_path = args[0]
    backup_folder = args[1]
    process_folder(folder_path,backup_folder)


if __name__=='__main__':
    usage = "usage: %prog [options] geojson_folder  backup_folder"
    parser = OptionParser(usage=usage, version="1.0 2017-4-16")

    (options, args) = parser.parse_args()

    main(options, args)