import matplotlib.pyplot as plt
import ctypes

data = open('out.txt', 'r').read().strip().split('\n')
data = [bytes.fromhex(x) for x in data]

screen_dim = (1920, 1080)

x, y = 0, 0
pts = []
for dat in data:
    button = dat[0]
    dx = dat[2]
    dy = dat[4]
    print(dat, button, dx, dy, x, y)

    if button == 1:
        x, y = zip(*pts)
        plt.plot(x, y)
        plt.show()
        x, y = 0, 0
        pts = [(x, y)]

    dx = ctypes.c_int8(dx).value
    dy = ctypes.c_int8(dy).value
    x = max(0, min(screen_dim[0], x + dx))
    y = max(0, min(screen_dim[1], y + dy))

    pts.append((x, y))

