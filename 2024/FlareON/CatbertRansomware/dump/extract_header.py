import ctypes

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

f = 'catmeme3.jpg.c4tb'
data = open(f, 'rb').read()
dec = decrypt_header(data)

enc = data[0x10:0x10+dec.enc_size]
vm = data[dec.vm_offset:dec.vm_offset+dec.vm_length]

print(vm)