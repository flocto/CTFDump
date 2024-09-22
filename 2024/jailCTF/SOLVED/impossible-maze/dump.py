#!/usr/bin/env python3
# Ref: https://github.com/HearthSim/UnityPack/issues/74

import sys
import os
from unitypack.utils import BinaryReader

SIGNATURE = 'UnityWebData1.0'

class DataFile:
    def load(self, file):
        buf = BinaryReader(file, endian="<")
        self.path = file.name

        self.signature = buf.read_string()
        header_length = buf.read_int()
        if self.signature != SIGNATURE:
            raise NotImplementedError('Invalid signature {}'.format(repr(self.signature)))

        self.blobs = []
        while buf.tell() < header_length:
            offset = buf.read_int()
            size = buf.read_int()
            namez = buf.read_int()
            name = buf.read_string(namez)
            self.blobs.append({ 'name': name, 'offset': offset, 'size': size })
        if buf.tell() > header_length:
            raise NotImplementedError('Read past header length, invalid header')

        for blob in self.blobs:
            buf.seek(blob['offset'])
            blob['data'] = buf.read(blob['size'])
            if len(blob['data']) < blob['size']:
                raise NotImplementedError('Invalid size or offset, reading past file')

if len(sys.argv) < 2:
    sys.exit(f'Usage: {sys.argv[0]} <UnityWebData1.0 file>')
    
unityWebDatafile = sys.argv[1]

f = open(unityWebDatafile, 'rb')
df = DataFile()
df.load(f)
EXTRACTION_DIR = 'extracted'
for blob in df.blobs:
    print('extracting @ {}:\t{} ({})'.format(blob['offset'], blob['name'], blob['size']))
    dest = os.path.join(EXTRACTION_DIR, blob['name'])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f:
        f.write(blob['data'])