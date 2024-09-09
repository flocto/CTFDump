import zipfile
import base64
import io

dat = b''
zf = zipfile.ZipFile('chunk_0.zip', 'r')

while True:
    tmp = None
    for file in zf.namelist():
        if file.endswith('.txt'):
            print(file)
            dat += zf.read(file)
        else:
            tmp = zf.read(file)
    
    if tmp is None:
        break
    else:
        # tmp becomes the next zip file in memory
        buf = io.BytesIO(tmp)
        zf = zipfile.ZipFile(buf, 'r')

open('data.txt', 'wb').write(dat)
print(dat)
open('out.bin', 'wb').write(base64.b64decode(dat))

# csawctf{ez_r3cur5iv3ne55_right7?}