from PIL import Image

img = Image.open('Terraria.gif')

print(img.n_frames, img.size)

N = 10

cross_section = Image.new('RGBA', (img.n_frames * N, img.size[0]))

for i in range(img.n_frames):
    img.seek(i)

    # put middle line horizontally from frame vertically on the cross section
    mid = img.size[1] // 2
    line = img.crop((0, mid, img.size[0], mid + 1))
    
    for j in range(N):
        for k in range(img.size[0]):
            cross_section.putpixel((i * N + j, k), line.getpixel((k, 0)))

cross_section.save('cross_section.png')

