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