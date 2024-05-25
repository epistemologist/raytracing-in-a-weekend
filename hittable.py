from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Optional

from utils import *
from ray import Ray

# Not making dataclass because I'm hoping to jit the shit out of this with numba and numba doesn't like dataclasses...
class HitRecord:
	def __init__(self, p: point3, normal: vec3, t: float):
		self.p = p
		self.normal = normal
		self.t = t

class Hittable(ABC):	
	@abstractmethod
	def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float) -> Optional[HitRecord]:
		pass

class Sphere(Hittable):
	def __init__(self, center: point3, radius: float):
		self.center = center
		self.radius = max(0, radius)
	def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float):
		OC = self.center - ray.origin
		a = length_squared( ray.direction )
		h = np.dot(r.direction, OC)
		c = length_squared(OC) - radius*radius

		discriminant = h*h - a*c
		if discriminant < 0: return None
		
		sqrtd = np.sqrt(discriminant)
		r1 = (h-sqrtd)/a; r2 = (h+sqrtd)/a
		for r in [r1, r2]:
			if ray_tmin <= r <= ray_tmax:
				t = r
				p = ray.at(t)
				normal = (p - center) / radius
				return HitRecord(
					t = t,
					p = p,
					normal = normal
				)
		return None
