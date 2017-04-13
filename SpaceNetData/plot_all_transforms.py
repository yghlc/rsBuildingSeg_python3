#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
def plot_all_transforms(input_image, pixel_coords, mask_image, dist_image, 
                        figsize=(8,8), plot_name='', add_global_title=False, 
                        colorbar=False, add_titles=False,
                        poly_face_color='orange', poly_edge_color='red', 
                        poly_nofill_color='blue', cmap='bwr'):
    '''Explore all transforms'''

    fig, (ax0, ax1, ax2, ax3) = plt.subplots(1, 4, 
                                        figsize=(4*figsize[0], figsize[1]))

    #fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(2*figsize[0], figsize[1]))
    
    if add_global_title:
        suptitle = fig.suptitle(plot_name.split('/')[-1], fontsize='large')

    # create patches
    patches = []
    patches_nofill = []
    if len(pixel_coords) > 0:
        # get patches    
        for coord in pixel_coords:
            patches_nofill.append(Polygon(coord, facecolor=poly_nofill_color, 
                                          edgecolor=poly_edge_color, lw=3))
            patches.append(Polygon(coord, edgecolor=poly_edge_color, fill=True, 
                                   facecolor=poly_face_color))
        p0 = PatchCollection(patches, alpha=0.25, match_original=True)
        p1 = PatchCollection(patches, alpha=0.75, match_original=True)
        p2 = PatchCollection(patches_nofill, alpha=0.75, match_original=True)
        
    #if len(patches) > 0:
    #    p0 = PatchCollection(patches, alpha=0.25, match_original=True)
    #    p1 = PatchCollection(patches, alpha=0.75, match_original=True)
                   
 
    # ax0: raw image
    ax0.imshow(input_image)
    if len(patches) > 0:
        ax0.add_collection(p0)
    if add_titles:
        ax0.set_title('Input Image + Ground Truth Buildings') 

    # truth polygons
    zero_arr = np.zeros(input_image.shape[:2])
    # set background to white?
    #zero_arr[zero_arr == 0.0] = np.nan
    ax1.imshow(zero_arr, cmap=cmap)
    if len(patches) > 0:
        ax1.add_collection(p2)
    if add_titles:
        ax1.set_title('Ground Truth Building Polygons')        

    # mask
    ax2.imshow(mask_image, cmap=cmap)
    # truth polygons?
    #if len(patches) > 0:
    #    ax1.add_collection(p1)
    if add_titles:
        ax2.set_title('Ground Truth Building Mask')    

    # distance transform
    cbar_pointer = ax3.imshow(dist_image)
    # overlay buildings on distance transform? 
    #if len(patches) > 0:
    #    ax3.add_collection(p1)
    if add_titles:
        #mind, maxd = np.round(np.min(dist_image),2), \
        #                                   np.round(np.max(dist_image),2)
        #dist_suffix = ""#" (min=" + str(mind) + ", max=" + str(maxd) + ")"
        #ax3.set_title("Yuan 2016 Distance Transform" + dist_suffix)
        ax3.set_title("Ground Truth Polygons Overlaid on Distance Transform")
    
    if colorbar:
        #from mpl_toolkits.axes_grid1 import make_axes_locatable
        #divider = make_axes_locatable(ax2)
        #cax = divider.append_axes('right', size='5%', pad=0.05)
        #fig.colorbar(cbar_pointer, cax=cax, orientation='vertical')
        left, bottom, width, height = [0.38, 0.85, 0.24, 0.03]
        cax = fig.add_axes([left, bottom, width, height])
        fig.colorbar(cbar_pointer, cax=cax, orientation='horizontal')

    #plt.axis('off')
    plt.tight_layout()
    if add_global_title:
        suptitle.set_y(0.95)
        fig.subplots_adjust(top=0.96)
    plt.show()
 
    if len(plot_name) > 0:
        plt.savefig(plot_name)
    
    return    