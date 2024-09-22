x = __builtins__.__dict__
valid = []
for f in x:
    if 'p' in f: continue
    if any([not c.islower() for c in f]): continue
    
    n = x[f]
    if callable(n):
        print(f)
        try:
            print('vars', vars(n))
        except:
            pass
        try:
            print('dir', dir(n))
        except:
            pass
        # try:
        #     print('format', format(n))
        # except:
        #     pass
        # try:
        #     print('format()', format(n()))
        # except:
        #     pass
        # valid.append(f)

# print(valid)

