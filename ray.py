import numpy as np
from dataclasses import dataclass
from typing import List

from util import *

@dataclass
class Ray:
	origin: vec3
	direction: vec3

	def at(self, t: float) -> vec3:
		return self.origin + t*self.direction
