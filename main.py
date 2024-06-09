from camera import *
from hittable import *

# World
world = HittableList(objects = [
	Sphere(point3([0,0,-1]), 0.5),
	Sphere(point3([0,-100.5,-1]), 100),
])

cam = Camera(image_width=1000)
cam.render(world)

