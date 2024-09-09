from flask import Flask, request
from pwn import remote
# nc cbc.ctf.csaw.io 9996
r = remote('cbc.ctf.csaw.io', 9996, level='error')
app = Flask(__name__)

def test(q):
    global r
    try:
        r.sendlineafter(b'ciphertext: ', q.encode())
        nxt = r.recvline()
        return nxt
    except Exception as e:
        r = remote('cbc.ctf.csaw.io', 9996, level='error')
        return test(q)

@app.get('/')
def hello():
    # q = request.args.get('q', '')
    q = request.cookies.get('q', '')
    # print(q)
    nxt = test(q)
    
    if b'Error' in nxt:
        return 'Error', 500
    
    print(q)
    return 'Looks fine'
    

if __name__ == '__main__':
    app.run(threaded=True, debug=False)