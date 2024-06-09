from math import inf
import numpy as np
from tqdm import tqdm

from util import *
from ray import Ray
from hittable import Hittable

class Camera:
	def __init__(self, aspect_ratio: float = 16./9, image_width: int = 400):
		# Image dimensions
		self.aspect_ratio = aspect_ratio
		self.image_width = image_width
		self.image_height = max(1, int(self.image_width / self.aspect_ratio))

		# Camera settings
		focal_length = 1
		viewport_height = 2.
		viewport_width = viewport_height * (self.image_width/self.image_height)
		self.camera_center = point3([0.,0.,0.])

		# Vectors along viewport edges
		viewport_u = vec3([ viewport_width, 0, 0 ])
		viewport_v = vec3([ 0, -viewport_height, 0 ])

		self.pixel_du = viewport_u / self.image_width
		self.pixel_dv = viewport_v / self.image_height

		viewport_upper_left = self.camera_center - vec3([0, 0, focal_length]) - viewport_u/2 - viewport_v/2
		self.P00_loc = viewport_upper_left + .5*(self.pixel_du + self.pixel_dv)

	def render(self, world: Hittable) -> None:
		X,Y = np.meshgrid( np.arange(self.image_width), np.arange(self.image_height) )
		PIXELS_X, PIXELS_Y, PIXELS_Z = (
			self.P00_loc[0] + X*self.pixel_du[0] + Y*self.pixel_dv[0],
			self.P00_loc[1] + X*self.pixel_du[1] + Y*self.pixel_dv[1],
			self.P00_loc[2] + X*self.pixel_du[2] + Y*self.pixel_dv[2],
		)

		def ray_trace(x,y,z):
			r = Ray(self.camera_center, np.array([x,y,z]))
			return self._ray_color(r, world) 
		ray_trace = np.vectorize(ray_trace)

		# PPM header
		print("P3")
		print(f"{self.image_width} {self.image_height}")
		print("255")
		
		for i in tqdm(range(self.image_height)):
			curr_line = ray_trace(
				PIXELS_X[i], PIXELS_Y[i], PIXELS_Z[i]	
			)
			for pixel in curr_line:
				r,g,b = unpack_color(pixel)
				print(f"{r} {g} {b}")

	def _ray_color(self, r: Ray, world: Hittable) -> int:
		rec: HitRecord = world.hit(r, Interval(0, inf))
		
		if rec is not None:
			return pack_color( 0.5 * (rec.normal + np.array([1.,1.,1.])) )

		unit_direction = unit_vector(r.direction)
		a = 0.5*(unit_direction[1]+1.)
		return pack_color( (1.-a)*np.array([1.,1.,1.]) + a*np.array([0.5,0.7,1.]) )
