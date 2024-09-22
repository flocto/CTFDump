# lines = open('level0.unity').read().split('\n')

# tilemap1 = lines[680:6286]
# open('tilemap1.txt', 'w').write('\n'.join(tilemap1))

# tilemap2 = lines[6286:13462]
# open('tilemap2.txt', 'w').write('\n'.join(tilemap2))

import yaml

def render_img(tiles, name):
    pos = {}
    for tile in tiles:
        x, y, z = tile['first']['x'], tile['first']['y'], tile['first']['z']
        idx = tile['second']['m_TileIndex']

        pos[(x, y)] = idx

    max_x = max(x for x, _ in pos)
    max_y = max(y for _, y in pos)
    min_x = min(x for x, _ in pos)
    min_y = min(y for _, y in pos)

    from PIL import Image
    import numpy as np

    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=np.uint8)

    for (x, y), idx in pos.items():
        img[max_y - y, x - min_x] = idx

    img = img * 255 // img.max()

    img = Image.fromarray(img, 'L')
    img.save(name)

tilemap1 = yaml.load(open('tilemap1.txt'), Loader=yaml.FullLoader)
tiles = tilemap1['Tilemap']['m_Tiles']
render_img(tiles, 'tilemap1.png')

tilemap2 = yaml.load(open('tilemap2.txt'), Loader=yaml.FullLoader)
tiles = tilemap2['Tilemap']['m_Tiles']
render_img(tiles, 'tilemap2.png')
