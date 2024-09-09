import matplotlib.pyplot as plt

data = open('dump.txt').readlines()
data = [eval(x.strip()) for x in data]

data = [(x, y, z, id) for (x, y, z, id) in data if id == 0]

x = [d[0] / 2 for d in data]
y = [d[1] for d in data]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x, y, s=10)
plt.ylim(50, 150)
plt.savefig('cormine1.png')