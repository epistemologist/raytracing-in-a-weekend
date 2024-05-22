import numpy as np
from dataclasses import dataclass

vec3 = np.array # NOTE: not checking length, assuming input == 3 

@dataclass
class Color:
	color: vec3
	
	def write_color(self):
		print(f"{int(256.*self.color[0])} {int(256.*self.color[1])} {int(256.*self.color[2])}")


@dataclass
class Ray:
	origin: vec3
	direction: vec3

	def at(t: float) -> vec3:
		return self.origin + t*self.direction
