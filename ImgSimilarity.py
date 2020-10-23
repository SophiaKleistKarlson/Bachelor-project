# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:29:15 2017

@author: semkt
"""

# import the necessary packages
#from skimage.measure import structural_similarity as ssim
import numpy as np
import pandas as pd
import cv2
import glob
import re
import os
import json

path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/"
os.chdir(path)
print(path)


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype(float) - imageB.astype(float)) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar" the two images are
    return err


def compare_images(imageA, imageB):
	# compute the mean squared error index for the images
    m = mse(imageA, imageB)
    return m
    
### load the images -- the originals and copies to compare

# path to folders
ORIG_path = 'data/transmission_eUZa0I1PpGMV_yQL0wCnLniwK/10/0/'#img/0/
COPY_path = 'data/transmission_eUZa0I1PpGMV_yQL0wCnLniwK/10/1/'#img/1/


# index for labels
ORIG_idx = len(ORIG_path)
COPY_idx = len(COPY_path)

# get file names
files_orig = glob.glob(ORIG_path + '*.png')#'cond_\d+_stim_\d+.png' if we don't want the tutorials
files_copy = glob.glob(COPY_path + '*.png')

print(files_orig)
print(files_copy)

# prepare panda to write logs
columns = ['Subject_ID', 'Chain', 'Generation', 'Condition', 'Stim_ID', 'Source_image', 'MSE'] # , 'SSIM' , 'master', 'copy', 'time', #
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)




# loop through originals and copies to compare and measure similarity 
for orig in files_orig:
    for copy in files_copy:
        # get labels (without path and extension) for match check
        orig_select = re.split('\.', orig[ORIG_idx:-1])[0]
        copy_select = re.split('\.', copy[COPY_idx:-1])[0]
        #print(copy_select)
        
        # check if they match
        if orig_select == copy_select:
            original = cv2.imread(orig)
            contrast = cv2.imread(copy)
            print(type(original))
            
            # convert the images to grayscale
            #original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            #contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
            
            # run similarity measures
            MSE = compare_images(original, contrast)#, SSIM
            
            # get id label
            #id = re.findall('cond_\d+_stim_\d+|tutorial\d+', copy)[0]
            chain = re.findall('(\d+)/\d', COPY_path)[0]
            gen = re.findall('\d+/(\d+)', COPY_path)[0]
            condition = re.findall('cond_\d+|tutorial\d+', copy)[0]# if we don't have tutorials, then we can just say cond_(\d+) 
            stim = re.findall('stim_(\d+)|tutorial\d+', copy)[0]
            
            # write output to pandas
            DATA = DATA.append({
                #'Subject_ID': id, 
                'Chain': chain,
                'Generation': gen,
                'Condition': condition[5],# if no tutorials, drop the index in the end
                'Stim_ID': stim,
                'MSE': MSE
                }, ignore_index=True)

print(DATA)

# save pandas
logfilename = "logfiles/SimilarityData4.csv"

DATA.to_csv(logfilename)            
