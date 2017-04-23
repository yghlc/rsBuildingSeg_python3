
#!/usr/bin/env python
# Filename: mat_To_png.py
"""
introduction: convert the deeplab result from mat to png

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 23 April, 2017
"""



from optparse import OptionParser
import os
import basic, io_function

import scipy.io as sio
import scipy.misc as misc
import numpy
from PIL import Image


def deeplabMat2png(mat_path):

    save_png = os.path.splitext(mat_path)[0] + '.png'
    data = sio.loadmat(mat_path)

    # raw_result = data.data;
    raw_result = data['data']
    raw_result = numpy.transpose(raw_result,[1,0,2,3])
    # raw_result = permute(raw_result, [2 1 3]);
    #
    img_row = 650 #; % size(img, 1);
    img_col = 650 #; % size(img, 2);
    #
    # result = raw_result(1:img_row, 1:img_col,:);
    result = raw_result[0:img_row, 0:img_col,:]

    # is_argmax = 0;
    # if ~is_argmax
    #     [~, result] = max(result, [], 3);
    #     result = uint8(result) - 1;
    # else
    #     result = uint8(result);
    # end

    is_argmax = 0;
    if ~is_argmax:
        # [value, result] = max(result, [], 3);
        result = numpy.argmax(result,axis=2)
        # result = numpy.uint8(result) - 1;
    else:
        result =numpy.uint8(result)


    result = numpy.uint8(result)
    result = result.reshape(img_row,img_col)

    result[numpy.where(result==1)] = 255
    # print result

    #
    # % imshow(result, [0, 1])
    # % imwrite(result, colormap, save_png);
    # result(find(result == 1)) = 255;
    # imwrite(result, save_png);

    # im = Image.fromarray(result)
    # im.save(save_png)

    misc.imsave(save_png,result)

    return True


def convert_mat_to_png(mat_folder):
    if os.path.isdir(mat_folder) is False:
        basic.outputlogMessage('mat_folder not exist: %s'%mat_folder)
        return False

    file_list = io_function.get_file_list_by_ext('.mat', mat_folder, bsub_folder=False)
    if len(file_list) < 0:
        basic.outputlogMessage('error, no mat found in ' + mat_folder)
        return False
    number = 0
    for matpath in file_list:
        number = number+1
        basic.outputlogMessage('%d / %d : %s'%(number,len(file_list),matpath))
        deeplabMat2png(matpath)

    return True

def main(options, args):
    # matpath = 'RGB-PanSharpen_AOI_2_Vegas_8bit_img4_blob_0.mat'

    #list file
    mat_folder = args[0]
    if os.path.isdir(mat_folder) is False:
        return False


if __name__=='__main__':
    usage = "usage: %prog [options] mat_folder"
    parser = OptionParser(usage=usage, version="1.0 2017-4-23")

    (options, args) = parser.parse_args()
    main(options, args)