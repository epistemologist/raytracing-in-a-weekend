from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Optional, List

from util import *
from ray import Ray

# Not making dataclass because I'm hoping to jit the shit out of this with numba and numba doesn't like dataclasses...
class HitRecord:
	def __init__(self, p: point3, normal: vec3, t: float):
		self.p = p
		self.normal = normal
		self.t = t
	def set_face_normal(self, ray: Ray, outward_normal: vec3):
		self.front_face = np.dot(ray.direction, outward_normal) < 0
		self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):	
	@abstractmethod
	def hit(self, ray: Ray, ray_t: Interval) -> Optional[HitRecord]:
		pass

class Sphere(Hittable):
	def __init__(self, center: point3, radius: float):
		self.center = center
		self.radius = max(0, radius)
	#def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float):
	def hit(self, ray: Ray, ray_t: Interval):
		OC = self.center - ray.origin
		a = length_squared( ray.direction )
		h = np.dot(ray.direction, OC)
		c = length_squared(OC) - self.radius*self.radius

		discriminant = h*h - a*c
		if discriminant < 0: return None
		
		sqrtd = np.sqrt(discriminant)
		r1 = (h-sqrtd)/a; r2 = (h+sqrtd)/a
		for r in [r1, r2]:
			if ray_t.contains(r):
				t = r
				p = ray.at(t)
				normal = (p - self.center) / self.radius
				rec = HitRecord(
					t = t,
					p = p,
					normal = normal
				)
				outward_normal = (rec.p - self.center)/self.radius
				rec.set_face_normal(ray, outward_normal)
				return rec
		return None

class HittableList(Hittable):
	def __init__(self, objects: Optional[List[Hittable]] ):
		self.objects: List[Hittable] = [] if objects is None else objects
	
	# append/clear objects by accessing the underlying list field
	def hit(self, ray: Ray, ray_t: Interval) -> Optional[HitRecord]:
		tmp_rec = None
		hit_anything = False
		closest_so_far = ray_t.b
		for obj in self.objects:
			curr_hit_rec = obj.hit( ray, Interval( ray_t.a, closest_so_far ) )
			if curr_hit_rec is not None:
				tmp_rec = curr_hit_rec
				hit_anything = True
				closest_so_far = curr_hit_rec.t		
		return tmp_rec
