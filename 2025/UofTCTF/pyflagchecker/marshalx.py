from marshal import load, loads as old_loads, dump, dumps as old_dumps
import marshal
import inspect
import importlib

def dump_pyc(fname, code):
    pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)
    with open(fname, 'wb') as f:
        f.write(pyc_data)

print(marshal)
# def __str__(self):
#     return "<module 'marshal' (built-in)>"

print('fake marshal loaded')
def loads(arg):
    print('loads called', len(arg), arg[:100])
    try:
        r = old_loads(arg)
        print('loaded', r)
        if len(arg) == 44463:
            dump_pyc('dump2.pyc', r)
        return r
    except Exception as e:
        print('error', e)
        return old_loads(arg)

s = open('sim.py').read()
c = open('chall.py').read()

def e(m):
    return bytes([a ^ b for a, b in zip(m, m[len(m) // 2:])])

def old_e(m, k):
    r = []
    r += [m[0]^(sum(k)&0o377)]
    for _, i in enumerate(m[1:]):
        k = e(k, [m[_]])
        r += [i^(sum(k)&0o377)]
    return bytes(r)

def dumps(arg):
    print('dumps called', len(arg))
    print(arg)
    if len(arg) > 3000:
        print('big')
        prev_frame = inspect.currentframe().f_back
        print('l2', prev_frame.f_locals['l2'])
    # if arg == s:
    #     print('sim.py')
    #     prev_frame = inspect.currentframe().f_back
    #     print('tb', prev_frame.f_locals['tb'])
    #     return old_dumps(c)
    # elif len(arg) == 98:
    #     return old_dumps(e.__code__.co_code)
    # elif len(arg) == 22:
    #     return old_dumps(inspect.getsource.__code__.co_code)
    # elif len(arg) == 102:
    #     return old_dumps(old_e.__code__.co_code)
    return old_dumps(arg)