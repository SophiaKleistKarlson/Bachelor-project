# -*- coding: utf-8 -*-
"""Image_preprocessing_script.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sor-lijj9Wq9nblue1dLeFmFOBT8990m

**Preprocessing script for images**

NB: The first couple of scripts are run locally on my own computer, before uploading resized images to google colaboratory

First, assign unique names to images using the csv created in the R preprocessing script
"""

"""
Created on Thu Nov 12, 2020

@author: Sophia Marthine Kleist Karlson
"""
## Script that renames drawings to unique names and puts them all in the same folder


# import the necessary packages
import pandas as pd
import cv2
import os

# set path
path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/data/"
os.chdir(path)
print(path)

# create folder for all images to be put in
if not os.path.exists('all_drawings'):
    os.makedirs('all_drawings')

# Import the csv file with image paths and unique names
Drawing_IDs = pd.read_csv('Drawing_IDs.csv')

# make the image path column to a list
image_path_list = Drawing_IDs[["image_path"]]
image_path_list = image_path_list["image_path"].tolist()

# make the image ID column to a list
image_ID_list = Drawing_IDs[["Drawing_ID"]]
image_ID_list = image_ID_list["Drawing_ID"].tolist()

# Loop that reads the image paths and saves them into the all_drawings folder with their unique names
for i in range(len(image_ID_list)):
    drawing = cv2.imread(image_path_list[i])
    drawing_ID = "all_drawings/" + image_ID_list[i] + ".png"
    cv2.imwrite(drawing_ID, drawing)

"""Now we resize all images to 400x400px"""

"""
Created on Fri Nov 13, 2020

@author: Sophia Marthine Kleist Karlson
"""
## Script that resizes drawings to be 400x400px and puts them all in the same folder


# load necessary modules
import cv2
import glob
import re
import os


# define path where all drawings are
path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/data/all_drawings/"
os.chdir(path)
print(path)

# make a list of all the drawings
img_list = glob.glob(path + "*.png")
img_list.sort() # sort the list alphabetically

print(len(img_list))

# make empty list to be filled with filenames
id = []

# make folder for the resized images
if not os.path.exists('all_resized_drawings'):
    os.makedirs('all_resized_drawings')


# loop that resizes each image to 400x400 px
for i in range(len(img_list)):
  id.append(re.findall('(Chain_\d+_Gen_\d+_Cond_\d+_Source_\d+).png', img_list[i])[0])
  src = cv2.imread(img_list[i], cv2.IMREAD_UNCHANGED)

  # set a new height and width in pixels
  new_height = 400
  new_width = 400

  # dsize
  dsize = (new_width, new_height)

  # resize image
  output = cv2.resize(src, dsize)
  
  # write the resized image and put it in the all_resized_drawings folder
  cv2.imwrite('C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/data/all_drawings/all_resized_drawings/{}.png'.format(id[i]), output)

"""The resized images are now uploaded to google colaboratory. These are blurred using cv.blur(), using the **averaging** function, and then converted to jpeg2000 format, the file sizes of which are put into a dataframe and saved as a csv. This csv as well as the blurred images and jpeg2000 files are zipped and downloaded"""

# import the necessary packages
import PIL
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import glob
import os
import re
import cv2
import cv2 as cv
from google.colab import files
from zipfile import ZipFile

# Define function
def complexity_comparison_function(img_list):
  
  # make directory to put jp2 files
  if not os.path.exists('jpeg_compressed_files_comparison'):
    os.makedirs('jpeg_compressed_files_comparison')

  # make directory to put blurred png files
  if not os.path.exists('blurred_images'):
    os.makedirs('blurred_images')
    
  # prepare dataframe
  columns = ['Stim_ID', 'Complexity_original', 'Complexity_convolution']
  index = np.arange(0)
  Complexity_comparison_data = pd.DataFrame(columns=columns, index = index)

  # list for id's
  id = []
  
  # convert png to jp2
  for i in range(len(img_list)):
    id.append(re.findall('/content/resized/(Chain_\d+_Gen_\d+_Cond_\d+_Source_\d+).png', img_list[i])[0]) 
    
    #complexity of original:
    img_original = Image.open(img_list[i])
    img_original.convert("RGBA").save("jpeg_compressed_files_comparison/Original_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
    
    # read image for blurring
    img_blur = cv.imread(img_list[i])

    # convolution
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(img_blur,-1,kernel)
    cv2.imwrite('/content/blurred_images/Convolution_{}.png'.format(id[i]), dst)

    # jpeg2000 convertion of blurred images
    img_convolution = Image.open("/content/blurred_images/Convolution_{}.png".format(id[i]))
    img_convolution.convert("RGBA").save("jpeg_compressed_files_comparison/Convolution_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])

  # list of original jp2 files
  img_jp2_original = glob.glob("jpeg_compressed_files_comparison/Original_*.jp2")
  img_jp2_original.sort() #important! Else the IDs and complexity scores won't match

  # list of convolution jp2 files
  img_jp2_convolution = glob.glob("jpeg_compressed_files_comparison/Convolution_*.jp2")
  img_jp2_convolution.sort()

  # save size and ID to dataframe
  for i in range(len(img_jp2_original)): 
    size_original = (Path(img_jp2_original[i]).stat().st_size)
    size_convolution = (Path(img_jp2_convolution[i]).stat().st_size)

    Complexity_comparison_data = Complexity_comparison_data.append({
      'Stim_ID': id[i],
      'Complexity_original': size_original, 
      'Complexity_convolution': size_convolution
    }, ignore_index=True)

  return Complexity_comparison_data


# define path where all drawings are
path = "/content/resized/" 
images = glob.glob(path + "*.png")
images.sort() #important! Else the IDs and complexity scores won't match

# run function on all drawings
complexity_comparison_data = complexity_comparison_function(images)

# print complexity scores and ID's
print(complexity_comparison_data)

# prepare logfilename and save
logfilename = "complexity_comparison.csv"
complexity_comparison_data.to_csv(logfilename)

# prepare zipfile
zipObj = ZipFile('image_processing.zip', 'w')

# add complexity_comparison.csv to the zipfile
zipObj.write('/content/complexity_comparison.csv')

# prepare lists of blurred images and jp2 files
#resized = glob.glob('/content/resized/' + "*.png")
blurred = glob.glob('/content/blurred_images/' + "*.png")
jpeg2000 = glob.glob('/content/jpeg_compressed_files_comparison/' + "*.jp2")

# loop over the blurred images and jp2 files and add them to the zipfile
for i in range(len(blurred)):
  # Add multiple files to the zipfile
  zipObj.write(blurred[i])
  zipObj.write(jpeg2000[i])
  #zipObj.write(resized[i])
  #zipObj.write('/content/jpeg_compressed_files_comparison/Convolution_Chain_0_Gen_0_Cond_0_Source_0.jp2')
  #zipObj.write('/content/jpeg_compressed_files_comparison/Convolution_Chain_1_Gen_1_Cond_1_Source_1.jp2')
  #zipObj.write('/content/blurred_images/Convolution_Chain_0_Gen_0_Cond_0_Source_0.png')
  #zipObj.write('/content/blurred_images/Convolution_Chain_1_Gen_1_Cond_1_Source_1.png')

# close the zipfile
zipObj.close()

# download zipfile
files.download("image_processing.zip")