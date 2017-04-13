#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Wed Dec 21 09:46:53 2016
@author: avanetten
"""

import matplotlib.pyplot as plt
import numpy as np
import shutil
import glob
import sys
import os

####################
####################
# EDIT THESE VALUES

# download spacenet utilities from:
#    https://github.com/SpaceNetChallenge/utilities/tree/master/python/spaceNet 
#  spacenet utils are not used here, but are used in craate_distance_map.py
#path_to_spacenet_utils = '.../spaceNetUtilities-master/python'
#sys.path.extend([path_to_spacenet_utils])
#from spaceNet import geoTools as gT

spacenet_explore_dir = '/Users/huanglingcao/codes/PycharmProjects/rsBuildingSeg/SpaceNetData'
sys.path.extend([spacenet_explore_dir])
import geojson_to_pixel_arr, create_dist_map, create_building_mask, \
        plot_truth_coords, plot_building_mask, plot_dist_transform, \
        plot_all_transforms

# set path to spacenet data
# acquire from: https://aws.amazon.com/public-datasets/spacenet/    
# spacenet_data_dir = '/Users/huanglingcao/Data/aws_SpaceNet/AOI_3_Paris_Train'
spacenet_data_dir = '/Users/huanglingcao/Data/aws_SpaceNet/ProcessedBuildingLabels'
  
# get N images in 3band data
N_ims = 7
  
####################
####################
    
###############################################################################
def main():   

    # imDir = spacenet_data_dir + '/RGB-PanSharpen/'
    # vecDir = spacenet_data_dir + '/geojson/buildings/'
    # imDir_out = spacenet_explore_dir + '/RGB-PanSharpen/'

    imDir = spacenet_data_dir + '/3band/'
    vecDir = spacenet_data_dir + '/vectorData/geoJson/'
    imDir_out = spacenet_explore_dir + '/3band/'

    ground_truth_patches = []
    pos_val, pos_val_vis = 1, 255
 
    ########################
    # Create directories

    #coordsDir = spacenet_explore_dir + 'pixel_coords_mask/'
    coords_demo_dir = spacenet_explore_dir + '/pixel_coords_demo/'

    maskDir = spacenet_explore_dir + '/building_mask/'
    maskDir_vis = spacenet_explore_dir + '/building_mask_vis/'
    mask_demo_dir = spacenet_explore_dir + '/mask_demo/'

    distDir = spacenet_explore_dir + '/distance_trans/'
    dist_demo_dir = spacenet_explore_dir + '/distance_trans_demo/'
    
    all_demo_dir = spacenet_explore_dir + '/all_demo/'

    # make dirs
    for p in [imDir_out, coords_demo_dir, maskDir, maskDir_vis, mask_demo_dir,
              distDir, dist_demo_dir, all_demo_dir]:
        if not os.path.exists(p):
            os.mkdir(p)

    # get input images and copy to working directory
    rasterList = glob.glob(os.path.join(imDir, '*.tif'))[0:0+N_ims]
    for im_tmp in rasterList:
        shutil.copy(im_tmp, imDir_out)
            
    # Create masks and demo images
    pixel_coords_list = []
    for i,rasterSrc in enumerate(rasterList):

        input_image = plt.imread(rasterSrc) # cv2.imread(rasterSrc, 1)
        print i, "rasterSrc:", rasterSrc
        
         # get name root
        name_root0 = rasterSrc.split('/')[-1].split('.')[0]
        # remove 3band or 8band prefix
        name_root = name_root0[6:]
        vectorSrc = vecDir +'Geo_' + name_root + '.geojson'
        maskSrc = maskDir + name_root0 + '.tif'
        
        ####################################################
        # pixel coords and ground truth patches
        pixel_coords, latlon_coords = \
            geojson_to_pixel_arr.geojson_to_pixel_arr(rasterSrc, vectorSrc, 
                                                      pixel_ints=True,
                                                      verbose=False)
        pixel_coords_list.append(pixel_coords)
       
        plot_name = coords_demo_dir + name_root + '.png'
        patch_collection, patch_coll_nofill = \
            plot_truth_coords.plot_truth_coords(input_image, pixel_coords,   
                  figsize=(8,8), plot_name=plot_name,
                  add_title=False)
        ground_truth_patches.append(patch_collection)
        ####################################################
        
        ####################################################
        #building mask
        outfile = maskDir + name_root0 + '.tif'
        outfile_vis = maskDir_vis + name_root0 + '.tif'
    
        # create mask from 0-1 and mask from 0-255 (for visual inspection)
        create_building_mask.create_building_mask(rasterSrc, vectorSrc, 
                                                  npDistFileName=outfile, 
                                                  burn_values=pos_val)
        create_building_mask.create_building_mask(rasterSrc, vectorSrc, 
                                                  npDistFileName=outfile_vis, 
                                                  burn_values=pos_val_vis)
        
        plot_name = mask_demo_dir + name_root + '.png'
        mask_image = plt.imread(outfile)    # cv2.imread(outfile, 0)
        plot_building_mask.plot_building_mask(input_image, pixel_coords,
                           mask_image,
                           figsize=(8,8), plot_name=plot_name,
                           add_title=False)     
        ####################################################   
        
        ####################################################
        # signed distance transform
        # remove 3band or 8band prefix
        outfile = distDir + name_root0 + '.npy'#'.tif'    
        create_dist_map.create_dist_map(rasterSrc, vectorSrc, 
                                        npDistFileName=outfile, 
                                        noDataValue=0, burn_values=pos_val, 
                                        dist_mult=1, vmax_dist=64)
        # plot
        plot_name = dist_demo_dir + name_root + '.png'
        mask_image = plt.imread(maskSrc)    # cv2.imread(maskSrc, 0)
        dist_image = np.load(outfile)
        plot_dist_transform.plot_dist_transform(input_image, pixel_coords, 
                                                dist_image, figsize=(8,8),
                                                plot_name=plot_name, 
                                                add_title=False)
        ####################################################

        ####################################################
        # plot all transforms
        plot_name = all_demo_dir + name_root + '_titles.png'
        mask_image = plt.imread(maskSrc)    # cv2.imread(maskSrc, 0)
        dist_image = np.load(outfile)
        plot_all_transforms.plot_all_transforms(input_image, pixel_coords, 
                                                mask_image, dist_image, 
                        figsize=(8,8), plot_name=plot_name, 
                        add_global_title=False, 
                        colorbar=False, 
                        add_titles=True,
                        poly_face_color='orange', poly_edge_color='red', 
                        poly_nofill_color='blue', cmap='bwr')        
        ####################################################

        
    # explore pixel_coords_list
    print "\nExplore pixel coords list..."
    print "pixel_coords_list[2][0]:", pixel_coords_list[2][0]

###############################################################################    
if __name__ == '__main__':
    main()              