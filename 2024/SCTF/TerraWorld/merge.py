from PIL import Image
import os

order = [
    'Terragrim',
    'Terrablade',
    'Terraspark',
    'Terrarian',
    'Terraprisma',
    'Terratoilet',
]

# for d in os.listdir('.'):
#     if os.path.isdir(d):
#         if d.startswith('Terra'):
#             print(d)
#             os.chdir(d)
#             frames = []
#             for i in range(1, 17):
#                 frames.append(Image.open(f'{i:02}.png'))
            
#             frames[0].save(f'../{d}.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
#             os.chdir('..')

frames = []
for d in order:
    print(d)
    os.chdir(d)
    for i in range(1, 17):
        frames.append(Image.open(f'{i:02}.png'))
    os.chdir('..')

frames[0].save(f'../Terraria.gif', save_all=True, append_images=frames[1:], duration=200, loop=0)