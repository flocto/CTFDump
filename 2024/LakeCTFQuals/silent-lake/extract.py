import zlib
import os

for file in os.listdir('glas/dot_codeql/precompiled/'):
    with open('glas/dot_codeql/precompiled/' + file, 'rb') as f:
        data = f.read()
        header, data = data[:0x10], data[0x10:]
        data = zlib.decompress(data)
        open('extracted/' + file, 'wb').write(data)

data = open('glas/example.qlx', 'rb').read()[989:]
open('extracted/example.qlx', 'wb').write(data)
header, data = data[:0x10], data[0x10:]
data = zlib.decompress(data)
open('extracted/example.ql', 'wb').write(data)