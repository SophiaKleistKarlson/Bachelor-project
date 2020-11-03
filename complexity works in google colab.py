import PIL
from PIL import Image

import glob
import os
import re

path = "/content/"
files = glob.glob(path + "*.png")
print(files)

if not os.path.exists('jpeg_compressed_files'):
    os.makedirs('jpeg_compressed_files')

im = []
jp2_name = []

for i in range(len(files)): 
  jp2_name.append(re.findall('/content/(stim_\d+).png', files[i]))
  # do something so that the jp2_name isn't a list of lists! it has to do with the name being a string??
  #jp2_name = re.findall('/content/(stim_\d+).png', files)[0] 
  # the commented out above doesn't work (you would delete the [i] after jp2_names in the .format() function, but it still doesn't work)
  img = Image.open(files[i])
  img.convert("RGBA").save("jpeg_compressed_files/{}.jp2".format(jp2_name[i]), 'JPEG2000', quality_mode='dB', quality_layers=[80])
  im.append(img)

print(jp2_name)
