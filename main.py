from defs import Color

from tqdm import tqdm
import numpy as np

image_width = image_height = 256
print("P3") # header
print(f"{image_width} {image_height}") # dimensions
print('255') # max color

for j in tqdm( range(image_height) ):
	for i in range( image_width ):
		pixel_color = Color( np.array( [
			1.*i / (image_width-1) , 1.* j / (image_height-1), 0
		]))
		pixel_color.write_color()


