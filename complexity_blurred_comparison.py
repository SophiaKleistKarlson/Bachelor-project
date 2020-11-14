# import the necessary packages
import PIL
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import glob
import os
import re

import cv2 as cv
from matplotlib import pyplot as plt


# Function
def complexity_comparison_function(img_list):
  
  # make directory to put jp2 files
  if not os.path.exists('jpeg_compressed_files_comparison'):
    os.makedirs('jpeg_compressed_files_comparison')
    
  # prepare dataframe
  columns = ['Stim_ID', 'Complexity_original', 'Complexity_convolution', 'Complexity_gaussian', 'Complexity_averaging']
  index = np.arange(0)
  Complexity_comparison_data = pd.DataFrame(columns=columns, index = index)

  # list for id's
  id = []
  
  # convert png to jp2
  for i in range(len(img_list)): 
    id.append(re.findall('/content/(Chain_\d+_Gen_\d+_Cond_\d+_Source_\d+).png', img_list[i])[0]) #change /content/ to /all_drawings/ if run on the computer

    #complexity of original:
    img_original = Image.open(img_list[i])
    img_original.convert("RGBA").save("jpeg_compressed_files_comparison/Original_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
    
    # read image for blurring
    img_blur = cv.imread(img_list[i])

    # convolution
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(img_blur,-1,kernel)
    cv2.imwrite('/content/Convolution_{}.png'.format(id[i]), dst)

    # gaussian
    gaussian = cv.GaussianBlur(img_blur,(5,5),0)
    cv2.imwrite('/content/Gaussian_{}.png'.format(id[i]), gaussian)

    # averaging
    blur = cv.blur(img,(5,5))
    cv2.imwrite('/content/Averaging_{}.png'.format(id[i]), blur)

    # jpeg2000 convertion of blurred images
    img_convolution = Image.open(dst)
    img_convolution.convert("RGBA").save("jpeg_compressed_files_comparison/Convolution_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])

    img_gaussian = Image.open(gaussian)
    img_gaussian.convert("RGBA").save("jpeg_compressed_files_comparison/Gaussian_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])

    img_averaging = Image.open(blur)
    img_averaging.convert("RGBA").save("jpeg_compressed_files_comparison/Averaging_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])


  # list of jp2 files
  img_jp2_original = glob.glob("jpeg_compressed_files_comparison/Original_*.jp2")
  img_jp2_original.sort() #important! Else the IDs and complexity scores won't match

  # list of jp2 files
  img_jp2_convolution = glob.glob("jpeg_compressed_files_comparison/Convolution_*.jp2")
  img_jp2_convolution.sort()

  # list of jp2 files
  img_jp2_gaussian = glob.glob("jpeg_compressed_files_comparison/Gaussian_*.jp2")
  img_jp2_gaussian.sort()

  # list of jp2 files
  img_jp2_averaging = glob.glob("jpeg_compressed_files_comparison/Averaging_*.jp2")
  img_jp2_averaging.sort()
  
  # save size and ID to dataframe
  for i in range(len(img_jp2_original)): 
    size_original = (Path(img_jp2_original[i]).stat().st_size)
    size_convolution = (Path(img_jp2_convolution[i]).stat().st_size)
    size_gaussian = (Path(img_jp2_gaussian[i]).stat().st_size)
    size_averaging = (Path(img_jp2_averaging[i]).stat().st_size)

    Complexity_comparison_data = Complexity_comparison_data.append({
      'Stim_ID': id[i],
      'Complexity_original': size_original, 
      'Complexity_convolution': size_convolution, 
      'Complexity_gaussian': size_gaussian, 
      'Complexity_averaging': size_averaging
    }, ignore_index=True)
  return Complexity_comparison_data


# define path where all drawings are
path = "/content/" # /all_drawings/
files = glob.glob(path + "*.png")

files.sort() #important! Else the IDs and complexity scores won't match
#print(files)

# run function on all drawings
complexity_comparison_data = complexity_comparison_function(files)

# print complexity scores and ID's
print(complexity_comparison_data)

# prepare logfilename and save
logfilename = "complexity_comparison.csv"
complexity_comparison_data.to_csv(logfilename)
