from pwn import xor

nums = list(map(int, '0 0 0 0 0 0 0 0 15 23 23 4 7 0 22 1 23 28 0 18 10 12 0 7 23 2 17 18 21 16 0 0 0 0 0 28 7 16 17 16 6 17 11 0 1 0 21 23 4 24 0 0 0 0 0 0'.split()))

print(nums, len(nums))

enc1 = b'csawctf{heres_anew_key_decrypt_the_secretto_reveal_flag}'

print(xor(enc1, nums))