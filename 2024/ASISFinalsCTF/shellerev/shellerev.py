LUT = 0x3A5C742E
def decrypt(block: int, key: int) -> int:
	"""
	Decrypts a 32-bit block of ciphertext using the KeeLoq algorithm.

	:param int block: 32-bit ciphertext block
	:param int key: 64-bit key
	:return: 32-bit plaintext block
	:rtype: int
	"""

	for i in range(528):
		# Calculate LUT key
		lutkey = (block >> 0) & 1 | (block >> 7) & 2 | (block >> 17) & 4 | (block >> 22) & 8 | (block >> 26) & 16

		# Calculate next bit to feed
		lsb = (block >> 31) ^ (block >> 15 & 1) ^ (LUT >> lutkey & 1) ^ (key >> 15 & 1)

		# Feed it
		block = (block & 0x7FFFFFFF) << 1 | lsb

		# Rotate key left
		key = (key & 0x7FFFFFFFFFFFFFFF) << 1 | key >> 63

	return block

A = 878633747
B = 938769594
key = (A << 32) | B

target_values = [384298162, -88548146, 349339073, 488498761, 242060753, 1436371157, 1709692819, -1016646918, -377917403]
target_values = [x & 0xFFFFFFFF for x in target_values]
target_values = [decrypt(x, key) for x in target_values]
print(b''.join([x.to_bytes(4, 'big') for x in target_values]))