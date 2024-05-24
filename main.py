from defs import *

from tqdm import tqdm
import numpy as np

def ray_color(r):
	unit_direction = r.direction
	unit_direction /= np.linalg.norm(unit_direction)
	a = 0.5*(1. + unit_direction[1])
	return pack_color( (1.-a)*np.array([1., 1., 1.]) + a*np.array([0.5, 0.7, 1.0]) )

aspect_ratio = 16. / 9.
image_width = 400

# Get image height
image_height = max( int(image_width / aspect_ratio), 1)

# Camera
focal_length = 1.
viewport_height = 2.
viewport_width = viewport_height * image_width/image_height
camera_center = point3([0,0,0]) 

# Vectors along viewport edges
viewport_u = vec3([ viewport_width, 0, 0 ]) 
viewport_v = vec3([ 0, -viewport_height, 0 ])

# Distance between pixels
pixel_du = viewport_u / image_width
pixel_dv = viewport_v / image_height

# Location of upper left pixel
viewport_upper_left = camera_center - vec3([0, 0, focal_length]) - viewport_u/2 - viewport_v/2

P00_loc = viewport_upper_left + .5 * (pixel_du + pixel_dv) 

print("P3") # header
print(f"{image_width} {image_height}") # dimensions
print('255') # max color

X, Y = np.meshgrid(np.arange(image_width), np.arange(image_height))

PIXELS_X, PIXELS_Y, PIXELS_Z = ( 
	P00_loc[0] + X * pixel_du[0] + Y * pixel_dv[0],
	P00_loc[1] + X * pixel_du[1] + Y * pixel_dv[1],
    P00_loc[2] + X * pixel_du[2] + Y * pixel_dv[2]
)

def ray_trace(x,y,z):
	r = Ray(camera_center, np.array([x,y,z]))
	return ray_color(r)

ray_trace = np.vectorize(ray_trace)

lines = []
for i in tqdm(range(image_height)):
	curr_line = ray_trace(
		PIXELS_X[i],
		PIXELS_Y[i],
		PIXELS_Z[i]
	)
	for pixel in curr_line:
		r, g, b = unpack_color(pixel)
		print(f"{r} {g} {b}")
