import numpy as np
from dataclasses import dataclass
from typing import List

vec3 = np.array # NOTE: not checking length, assuming input == 3 
point3 = vec3

unit_vector = lambda v: v / np.linalg.norm(v)

class Color:	
	def __init__(self, color: vec3):
		self.color = color
	
	def write_color(self):
		print(f"{int(256.*self.color[0])} {int(256.*self.color[1])} {int(256.*self.color[2])}")

def pack_color(c: vec3) -> int:
	r = min( 255, int(256. * c[0]) )
	g = min( 255, int(256. * c[1]) )
	b = min( 255, int(256. * c[2]) )
	return (r<<16) | (g<<8) | b

def unpack_color(n: int) -> List[int]:
	return [
		(n & (255<<16)) >> 16,
		(n & (255<<8)) >> 8,
		n & 255
	]

@dataclass
class Ray:
	origin: vec3
	direction: vec3

	def at(self, t: float) -> vec3:
		return self.origin + t*self.direction
