#!/usr/bin/env python2
# Filename: test_models 
"""
introduction: test the models in this project

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 13 April, 2017
"""

# import basic.RSImage as RSImage
from basic.RSImage import RSImageclass
from basic.RSImageProcess import  RSImgProclass
import basic.basic as basic
import numpy


def test_plot_truth_coords():
    import SpaceNetData.plot_truth_coords as ptcoords
    import SpaceNetData.geojson_to_pixel_arr as geojson_to_pixel_arr

    img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/RGB-PanSharpen/RGB-PanSharpen_AOI_3_Paris_img183.tif"
    # img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/PAN/PAN_AOI_3_Paris_img183.tif"
    geojson = '/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/geojson/buildings/buildings_AOI_3_Paris_img183.geojson'

    pixel_coords, latlon_coords = \
        geojson_to_pixel_arr.geojson_to_pixel_arr(img_path,geojson,pixel_ints=True,verbose=True)

    # img_obj = RSImageclass()
    # if img_obj.open(img_path) is False:
    #     basic.outputlogMessage('Open image %s failed'%img_path)
    #     return False
    # Datatype = img_obj.GetGDALDataType()
    # width = img_obj.GetWidth()
    # height = img_obj.GetHeight()
    img_pro_obj = RSImgProclass()
    input_image_band1 =img_pro_obj.Read_Image_band_data_to_numpy_array_all_pixel(1,img_path)
    print numpy.min(input_image_band1), numpy.max(input_image_band1)
    input_image_band1 = (input_image_band1- numpy.min(input_image_band1))*1.0/(numpy.max(input_image_band1) - numpy.min(input_image_band1))
    print numpy.min(input_image_band1),numpy.max(input_image_band1)
    print input_image_band1.shape
    input_image_band2 = img_pro_obj.Read_Image_band_data_to_numpy_array_all_pixel(2, img_path)
    input_image_band2 = (input_image_band2 - numpy.min(input_image_band2)) * 1.0 / (numpy.max(input_image_band2) - numpy.min(input_image_band2))
    print numpy.min(input_image_band2), numpy.max(input_image_band2)
    print input_image_band2.shape
    input_image_band3 = img_pro_obj.Read_Image_band_data_to_numpy_array_all_pixel(3, img_path)
    input_image_band3 = (input_image_band3 - numpy.min(input_image_band3)) * 1.0 / (numpy.max(input_image_band3) - numpy.min(input_image_band3))
    print numpy.min(input_image_band3), numpy.max(input_image_band3)
    print input_image_band3.shape

    if input_image_band1 is False:
        basic.outputlogMessage('Open image %s failed' % img_path)
        return False
    input_image = numpy.stack((input_image_band1,input_image_band2,input_image_band3),axis=2)
    # input_image = input_image_band1
    # input_image.reshape(650,650,3)
    input_image = input_image.astype(numpy.float32)   # the value of each pixel is between 0-1
    print input_image.shape

    ptcoords.plot_truth_coords(input_image,pixel_coords)


    pass


def test_create_building_mask():
    import SpaceNetData.create_building_mask as create_building_mask

    img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/RGB-PanSharpen/RGB-PanSharpen_AOI_3_Paris_img183.tif"
    # img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/PAN/PAN_AOI_3_Paris_img183.tif"
    geojson = '/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/geojson/buildings/buildings_AOI_3_Paris_img183.geojson'

    create_building_mask.create_building_mask(img_path,geojson,npDistFileName='out.tif')

def test_create_dist_map():
    import SpaceNetData.create_dist_map as create_dist_map

    img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/RGB-PanSharpen/RGB-PanSharpen_AOI_3_Paris_img183.tif"
    # img_path = "/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/PAN/PAN_AOI_3_Paris_img183.tif"
    geojson = '/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train/geojson/buildings/buildings_AOI_3_Paris_img183.geojson'

    create_dist_map.create_dist_map(img_path,geojson,npDistFileName='dist_out.tif')



def main():
    # test_plot_truth_coords()

    # test_create_building_mask()

    test_create_dist_map()


    pass

if __name__=='__main__':
    main()
