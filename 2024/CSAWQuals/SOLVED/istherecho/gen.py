from PIL import Image, ImageChops

def gen_diff(img1, img2):
    im1 = Image.open(img1)
    im2 = Image.open(img2)
    # xor the images, except for the alpha channel
    diff = ImageChops.difference(im1.convert('RGB'), im2.convert('RGB'))
    diff.save('diff.png')
    return diff

gen_diff('dump/measure_0.png', 'dump/measure_1.png')