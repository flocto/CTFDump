import ctypes

openssl = ctypes.CDLL('libcrypto.so')
zlib = ctypes.CDLL('libz.so')

enc = open('file.bin', 'rb').read()

key = b'by_4dd1ng_nd_multiply1ng_w3_pl4y_4_l1ttl3_m3l0dy'[:32]
iv = b'\x8c\xa2\xca\xb2)\xdba\n\xac\xdd\x9dC|az\xf3'

# 0040181d        int64_t rax_1 = malloc(bytes: size)
# 00401825        int64_t rax_2 = EVP_CIPHER_CTX_new()
# 00401830        int32_t var_400170
# 00401830        
# 00401830        if (rax_2 != 0 && EVP_DecryptInit_ex(rax_2, EVP_aes_256_cbc(), 0, &flag, &iv) == 1
# 00401830                && EVP_DecryptUpdate(rax_2, rax_1, &var_400170, &MEM, zx.q(size.d)) == 1
# 00401830                && EVP_DecryptFinal_ex(rax_2, sx.q(var_400170) + rax_1, &var_400170) == 1)
# 0040189c            EVP_CIPHER_CTX_free(rax_2)
# 004018b7            var_400170.q = compressBound(0x100000)
# 004018c3            uncompress(&MEM, &var_400170, rax_1, size)
# 004018cb            free(mem: rax_1)

size = ctypes.c_size_t(len(enc))
mem = ctypes.create_string_buffer(size.value)
mem.value = enc
ctx = openssl.EVP_CIPHER_CTX_new()

key_buf = ctypes.create_string_buffer(key)
iv_buf = ctypes.create_string_buffer(iv)

openssl.EVP_DecryptInit_ex(ctx, openssl.EVP_aes_256_cbc(), None, key_buf, iv_buf)