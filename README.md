# Raytracer in a Weekend

Implementing a raytracer in Python
Some notes:
 - using numpy for vector manipulation instead of vec3 class
 - `hittable.hit` originally returns `bool`, instead `Hittable.hit` returns an `Optional[HitRecord]`
