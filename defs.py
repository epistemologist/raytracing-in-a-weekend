import numpy as np
from dataclasses import dataclass

vec3 = np.array

@dataclass
class Color:
	color: vec3
	
	def write_color(self):
		print(f"{int(256.*self.color[0])} {int(256.*self.color[1])} {int(256.*self.color[2])}")
