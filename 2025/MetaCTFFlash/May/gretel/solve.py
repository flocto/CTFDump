from Crypto.Cipher import AES

enc = bytes.fromhex('c41fb50049ffbee51fc2620abeb88bfcd7802183967d29e4c5941cd969e664cb')

# template <typename CHAR_TYPE>
# constexpr void cipher(CHAR_TYPE* data, size_type size, key_type key)
# {
# 	// Obfuscate with a simple XOR cipher based on key
# 	for (size_type i = 0; i < size; i++)
# 	{
# 		data[i] ^= CHAR_TYPE((key >> ((i % 8) * 8)) & 0xFF);
# 	}
# }
def cipher(data: bytes, key: int) -> bytes:
    # Obfuscate with a simple XOR cipher based on key
    return bytes([data[i] ^ ((key >> ((i % 8) * 8)) & 0xFF) for i in range(len(data))])

enc_key = b'\xec\xe0]\xdd\xff\x1b3M\xb9\xb3\x0b\x80\xad\x1c?G\xef\xb2]\xdc\xfdH5B\xee\xb2\\\x81\xf3\x1adA\xdd'
key = 8432754782978560477
dec_key = cipher(enc_key, key)[:32].decode()
dec_key = bytes.fromhex(dec_key)
print(dec_key)

enc_iv = b'tT\x08\xecA?\x8c\xdevW\t\xef\x15;\x89\xd1w\x00\x08\xbd\x179\xd9\x85\'R\x05\xecA>\xd9\xd6\x45'
key = 16699080408112640325
dec_iv = cipher(enc_iv, key)[:32].decode()
dec_iv = bytes.fromhex(dec_iv)

cipher = AES.new(dec_key, AES.MODE_CBC, iv=dec_iv)
dec = cipher.decrypt(enc)
print(dec)