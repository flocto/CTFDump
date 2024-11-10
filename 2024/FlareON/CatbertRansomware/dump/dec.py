from Crypto.Cipher import ARC4
import sys
import ctypes
from zlib import crc32


class decrypt_struct(ctypes.Structure):
    _fields_ = [
        ("magic", ctypes.c_char * 4),
        ("enc_size", ctypes.c_uint32),
        ("vm_offset", ctypes.c_uint32),
        ("vm_length", ctypes.c_uint32),
        # ("vm_ptr", ctypes.c_void_p),
        # ("enc_ptr", ctypes.c_void_p),
    ]


def decrypt_header(data):
    dec = decrypt_struct.from_buffer_copy(data)
    print(dec.magic)
    print(dec.enc_size)
    print(dec.vm_offset)
    print(dec.vm_length)
    return dec


if __name__ == '__main__':
    fname, key = sys.argv[1], sys.argv[2]
    # enc = open('DilbootApp.efi.enc', 'rb').read()
    if fname == 'DilbootApp.efi.enc':
        keys = [b'DaCubicleLife101',
                b'G3tDaJ0bD0neM4te',
                b'VerYDumBpassword']
        
        # *_dilboot_key = img3_decrypted[7];
        #   _dilboot_key[1] = _img3[5];
        #   _dilboot_key[2] = _img3[2];
        #   _dilboot_key[3] = _img3[1];
        #   _img1 = img1_decrypted;
        #   _dilboot_key[4] = img1_decrypted[1];
        #   _dilboot_key[5] = _img3[5];
        #   _dilboot_key[6] = _img1[6];
        #   _dilboot_key[7] = _img3[2];
        #   _dilboot_key[8] = _img1[1];
        #   _dilboot_key[9] = _img1[6];
        #   _dilboot_key[10] = _img3[3];
        #   _dilboot_key[11] = _img1[13] + 3;
        #   _dilboot_key[12] = _img1[9];
        #   _dilboot_key[13] = _img1[10];
        #   _dilboot_key[14] = _img1[11];
        #   _dilboot_key[15] = _img1[12];
        key = bytearray(16)
        key[0] = keys[2][7]
        key[1] = keys[2][5]
        key[2] = keys[2][2]
        key[3] = keys[2][1]
        key[4] = keys[0][1]
        key[5] = keys[2][5]
        key[6] = keys[0][6]
        key[7] = keys[2][2]
        key[8] = keys[0][1]
        key[9] = keys[0][6]
        key[10] = keys[2][3]
        key[11] = keys[0][13] + 3
        key[12] = keys[0][9]
        key[13] = keys[0][10]
        key[14] = keys[0][11]
        key[15] = keys[0][12]

        print(key)

        enc = open(fname, 'rb').read()
        rc4 = ARC4.new(bytes(key))
        dec = rc4.decrypt(enc)
        open('DilbootApp.efi', 'wb').write(dec)
        sys.exit(0)

    enc = open(fname, 'rb').read()
    header = decrypt_header(enc[:0x10])

    enc = enc[0x10:0x10+header.enc_size]

    rc4 = ARC4.new(key.encode())
    dec = rc4.decrypt(enc)

    dec_fname = fname.rsplit('.', 1)[0]

    open(dec_fname, 'wb').write(dec)
