from tqdm import tqdm

image_width = image_height = 256
print("P3") # header
print(f"{image_width} {image_height}") # dimensions
print('255') # max color

for i in tqdm( range(image_width) ):
	for j in range( image_height ):
		print(f"{i} {j} {0}")

