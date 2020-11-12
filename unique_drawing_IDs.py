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
path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/"
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
