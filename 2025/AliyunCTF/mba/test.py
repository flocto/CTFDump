basises = [0, 0, 0, 0,   
-1, -1, 1, 1, 
0, 1, -1, 0,  
-1, 0, 0, 1,  
1, 0, -1, 0,  
0, -1, 0, 1,  
1, 1, -2, 0,  
0, 0, -1, 1,  
0, 0, 1, 0,   
-1, -1, 2, 1, 
0, 1, 0, 0,   
-1, 0, 1, 1,  
1, 0, 0, 0,   
0, -1, 1, 1,
1, 1, -1, 0,
0, 0, 0, 1]

basis = [basises[i:i+4] for i in range(0, len(basises), 4)]

for i in range(len(basis)):
    _basis = basis[i]
    print(i, _basis)
    for x in [False, True]:
        for y in [False, True]:
            x_and_y = x and y

            s = 0
            if x:
                s += _basis[0]
            if y:
                s += _basis[1]
            if x_and_y:
                s += _basis[2]
            s += _basis[3]
            print(x, y, s)
    print()

