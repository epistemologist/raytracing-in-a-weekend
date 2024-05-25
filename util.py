import numpy as np
from math import inf
from dataclasses import dataclass
from typing import List, Optional

vec3 = np.array # NOTE: not checking length, assuming input == 3 
point3 = vec3

length = lambda v: np.linalg.norm(v) 
length_squared = lambda v: (v**2).sum()
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

class Interval:
	def __init__(self, a: Optional[float], b: Optional[float]):
		if a is None or b is None:
			self.a = -inf; self.b = inf
		else:
			self.a = a; self.b = b

	def size(self) -> float:
		return self.b - self.a
	
	def contains(self, x: float) -> bool:
		return self.a <= x <= self.b
	
	def surrounds(self, x: float) -> bool:
		return self.a < x < self.b

Interval.EMPTY = Interval(inf, -inf)
Interval.UNIVERSE = Interval(-inf, inf)

