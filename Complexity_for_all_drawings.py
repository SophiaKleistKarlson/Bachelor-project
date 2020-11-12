"""
Created on Thu Nov 12, 2020

@author: Sophia Marthine Kleist Karlson
"""

## Complexity function for all drawings


# import the necessary packages
import PIL
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import glob
import os
import re


# Function
def complexity_function(img_list):
  
  # make directory to put jp2 files
  if not os.path.exists('jpeg_compressed_files'):
    os.makedirs('jpeg_compressed_files')
    
  # prepare dataframe
  columns = ['Stim_ID', 'Complexity']
  index = np.arange(0)
  Complexity_data = pd.DataFrame(columns=columns, index = index)

  # list for id's
  id = []
  
  # convert png to jp2
  for i in range(len(img_list)): 
    id.append(re.findall('/content/(Chain_\d+_Gen_\d+_Cond_\d+_Source_\d+).png', img_list[i])[0])# change /content/ to /all_drawings/ if run on the computer
    img = Image.open(img_list[i])
    img.convert("RGBA").save("jpeg_compressed_files/{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
  
  # list of jp2 files
  img_jp2 = glob.glob("jpeg_compressed_files/*.jp2")
  img_jp2.sort() #important! Else the IDs and complexity scores won't match
  
  # save size and ID to dataframe
  for i in range(len(img_jp2)): 
    size = (Path(img_jp2[i]).stat().st_size)
    Complexity_data = Complexity_data.append({
    'Stim_ID': id[i],
    'Complexity': size
  }, ignore_index=True)
  return Complexity_data


# define path where all drawings are
path = "/content/" # /all_drawings/
files = glob.glob(path + "*.png")

files.sort() #important! Else the IDs and complexity scores won't match
#print(files)

# run function on all drawings
complexity_data = complexity_function(files)

# print complexity scores and ID's
print(complexity_data)

# prepare logfilename and save
logfilename = "all_drawings_complexity.csv"
complexity_data.to_csv(logfilename)
