x = ''':nth-child(223),
        :nth-child(90),
        :nth-child(248),
        :nth-child(159),
        :nth-child(138),
        :nth-child(87),
        :nth-child(96),
        :nth-child(221),
        :nth-child(241),
        :nth-child(217),
        :nth-child(122),
        :nth-child(179),
        :nth-child(148),
        :nth-child(246),
        :nth-child(162),
        :nth-child(232),
        :nth-child(84),
        :nth-child(107),
        :nth-child(73),
        :nth-child(167),
        :nth-child(186),
        :nth-child(178),
        :nth-child(101),
        :nth-child(202),
        :nth-child(256),
        :nth-child(103),
        :nth-child(219),
        :nth-child(78),
        :nth-child(230),
        :nth-child(166),
        :nth-child(75),
        :nth-child(160),
        :nth-child(261),
        :nth-child(163),
        :nth-child(210),
        :nth-child(249),
        :nth-child(185),
        :nth-child(182),
        :nth-child(263),
        :nth-child(143),
        :nth-child(80),
        :nth-child(214),
        :nth-child(169),
        :nth-child(204),
        :nth-child(229),
        :nth-child(152),
        :nth-child(240),
        :nth-child(180),
        :nth-child(161),
        :nth-child(69),
        :nth-child(255),
        :nth-child(92),
        :nth-child(141),
        :nth-child(106),
        :nth-child(228),
        :nth-child(79),
        :nth-child(105),
        :nth-child(67),
        :nth-child(86),
        :nth-child(89),
        :nth-child(238),
        :nth-child(95),
        :nth-child(72),
        :nth-child(174),
        :nth-child(198),
        :nth-child(242),
        :nth-child(156),
        :nth-child(68),
        :nth-child(206),
        :nth-child(88),
        :nth-child(188),
        :nth-child(253),
        :nth-child(251),
        :nth-child(220),
        :nth-child(222),
        :nth-child(147),
        :nth-child(262),
        :nth-child(215),
        :nth-child(236),
        :nth-child(226),
        :nth-child(189),
        :nth-child(233)'''

bits = []
for line in x.split('\n'):
    b = int(line.split(':nth-child(')[1].split(')')[0]) 
    bits.append(b)

bits.sort()
bits = [x - 64 for x in bits]
print(bits)

b = [0] * 200
for i in bits:
    b[i] = 1

x = ''.join([str(x) for x in b])
print(x)

for i in range(0, len(x), 8):
    print(x[i:i+8], end=' ')

# x = int(x, 2)
# x = x.to_bytes((x.bit_length() + 7) // 8, 'little')
# print(x.hex())