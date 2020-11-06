### Note that this is 4 scripts that should be run individually in jupyter notebook/google colab

# 1: black pixel calculater
import PIL
from PIL import Image

import re
import glob
import os
import numpy as np
import pandas as pd

images = glob.glob("/content/" + '*.png')
images.sort()
print(images)

columns = ['Stim_ID', 'Black_px']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)

#id = [1,10,11,12,2,3,4,5,6,7,8,9]
black_px = []
id = []

for i in range(12):
  img = Image.open(images[i])
  #id = re.findall("/content/stim_(\d+).png", images[i])
  id.append(int(re.findall('/content/stim_(\d+).png', images[i])[0]))
  black_px = (len([px for px in list(img.getdata()) if px[1] < 0.01]))
  DATA = DATA.append({
    'Stim_ID': id[i],
    'Black_px': black_px
  }, ignore_index=True)

print(DATA)
logfilename = "black_px.csv"
DATA.to_csv(logfilename)



# 2: complexity loop
import PIL
from PIL import Image

import glob
import os
import re

path = "/content/"
files = glob.glob(path + "*.png")
files.sort()
print(files)

if not os.path.exists('jpeg_compressed_files'):
    os.makedirs('jpeg_compressed_files')

im = []
jp2_name = []

for i in range(len(files)): 
  jp2_name.append(int(re.findall('/content/stim_(\d+).png', files[i])[0]))
  img = Image.open(files[i])
  img.convert("RGBA").save("jpeg_compressed_files/stim_{}.jp2".format(jp2_name[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
  im.append(img)

print(im)
print(jp2_name)



# 3: or, as a function:
import PIL
from PIL import Image
from pathlib import Path
import glob
import os
import re

# Function
def complexity_function(img_list):
  if not os.path.exists('jpeg_compressed_files'):
    os.makedirs('jpeg_compressed_files')
  id = []
  for i in range(len(img_list)): 
    id.append(int(re.findall('/content/stim_(\d+).png', img_list[i])[0]))
    img = Image.open(img_list[i])
    img.convert("RGBA").save("jpeg_compressed_files/stim_{}.jp2".format(id[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
  img_jp2 = glob.glob("jpeg_compressed_files/*.jp2")
  img_jp2.sort()
  print(img_jp2)
  print(type(img_jp2))
  size = []
  for i in range(len(img_jp2)): 
    size.append(Path(img_jp2[i]).stat().st_size)
  return size

path = "/content/"
files = glob.glob(path + "*.png")
#files.sort()
print(files)

complexity_function(files)




#4: Combining both

import PIL
from PIL import Image

import re
import glob
import os
import numpy as np
import pandas as pd

images = glob.glob("/content/" + '*.png')
images.sort()
print(images)

columns = ['Stim_ID', 'Black_px', 'Complexity']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)

#id = [1,10,11,12,2,3,4,5,6,7,8,9]
black_px = []
id = []
size = complexity_function(images)

for i in range(12):
  img = Image.open(images[i])
  #id = re.findall("/content/stim_(\d+).png", images[i])
  id.append(int(re.findall('/content/stim_(\d+).png', images[i])[0]))
  black_px = (len([px for px in list(img.getdata()) if px[1] < 0.01]))
  DATA = DATA.append({
    'Stim_ID': id[i],
    'Black_px': black_px, 
    'Complexity': size[i]
  }, ignore_index=True)

print(DATA)
logfilename = "source_image_info.csv"
DATA.to_csv(logfilename)

