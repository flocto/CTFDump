from PIL import Image

# 128 by 128 black image
img = Image.new('RGB', (128, 256), color = 'white')

# save as tiff
img.save('blank2.tiff')
