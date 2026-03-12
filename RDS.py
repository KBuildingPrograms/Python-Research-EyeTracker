 # -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 10:36:20 2025

@author: kawdi
"""
#rds generation for pynotebook from Greydanus GITHUB
#found this while looking through documentation before using gpt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys
import os

def resources_path(relative_path): #path guide for Pyinstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

masks = ["Photos/cylinder_mask.png","Photos/sphere_mask.png","Photos/cube_mask.png","Photos/cone_mask.png"]

def random_dot(mask_name, pattern_reps=1, invert=False):
    invert_factor = -1 if invert else 1
    
    depth_mask = Image.open(resources_path(mask_name)).convert("RGB")
    depth_mask_data = depth_mask.load()
    depth_mask.save("rgb.png")
    
    pattern_w = depth_mask.size[0] / pattern_reps
    pattern_w = int(pattern_w)
    pattern_h = depth_mask.size[1]
    
    pattern = np.random.randint(0,256,(pattern_w,pattern_h))
    pattern2 = np.transpose(pattern)
    pattern_img = Image.fromarray(pattern2)

    
    output = Image.new("L", depth_mask.size)
    output_array = np.array(output)
    output_array = np.transpose(output_array)
#output_data = output.load()
    
    for x in range(0, depth_mask.size[0]):
        for y in range(0, depth_mask.size[1]):
            shift = 10 * (depth_mask_data[x,y][0] / 255)
            shift = int(shift)
            xp = x + (shift*invert_factor)
            output_array[x,y]= pattern[xp,y]
    output_array = np.transpose(output_array)
    output = Image.fromarray(output_array)
    
    total_x = int(output.size[0] * 2.1)
    total_y = output.size[1]
    img = Image.new("RGB",(total_x,total_y),(255,255,255))
    img.paste(output,(total_x-output.size[0],0))
    img.paste(pattern_img,(0,0))
    return img



def individuals_RDS(mask_name,in_shift,pattern_reps=1, invert=False):
    invert_factor = -1 if invert else 1
    
    depth_mask = Image.open(resources_path(mask_name)).convert("RGB")
    depth_mask_data = depth_mask.load()
    depth_mask.save("rgb.png")
    
    pattern_w = depth_mask.size[0] / pattern_reps
    pattern_w = int(pattern_w)
    pattern_h = depth_mask.size[1]
    
    pattern = np.random.randint(0,256,(pattern_w,pattern_h))
    
    pattern2 = np.transpose(pattern)
    pattern_img = Image.fromarray(pattern2)

    
    output = Image.new("L", depth_mask.size)
    output_array = np.array(output)
    output_array = np.transpose(output_array)
#output_data = output.load()
    
    for x in range(0, depth_mask.size[0]):
        for y in range(0, depth_mask.size[1]):
            shift = (10 * (depth_mask_data[x,y][0] / 255))*in_shift
            shift = int(shift)
            xp = x + (shift*invert_factor)
            output_array[x,y]= pattern[xp,y]
    output_array = np.transpose(output_array)
    output = Image.fromarray(output_array)
    
    img_off = pattern2
    img_on = output_array
    
    return img_on,img_off


def gray(im): #turns images to grayscale for the random dot stereogram
    #from eyllanesc on stack overflow
    im = 255 * (im / im.max())
    w, h = im.shape
    ret = np.empty((w,h,3),dtype=np.uint8)
    ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = im
    return ret


