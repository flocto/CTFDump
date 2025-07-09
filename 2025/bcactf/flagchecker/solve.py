def validate_flag(flag_bytes):
    if len(flag_bytes) != 44:
        return False
    
    # Round 1: bytes 0-15
    key1_a = 0xa8b576e88daae1c2885f77f57702fa15
    key1_b = 0xc5d71484f8cf9bf4b76f47904730804b
    
    for i in range(16):
        byte_val = flag_bytes[i]
        key_byte_a = (key1_a >> (8 * (15 - i))) & 0xff
        key_byte_b = (key1_b >> (8 * (15 - i))) & 0xff
        expected = key_byte_a ^ key_byte_b
        if byte_val != expected:
            return False
    
    # Round 2: bytes 16-31
    key2_a = 0x10659bdc6368e83dd4d62a13f3523aa1
    key2_b = 0x9e3225a9f133b5dea168f4e2851f072f
    
    for i in range(16):
        byte_val = flag_bytes[16 + i]
        key_byte_a = (key2_a >> (8 * (15 - i))) & 0xff
        key_byte_b = (key2_b >> (8 * (15 - i))) & 0xff
        expected = key_byte_a + key_byte_b
        if (byte_val & 0xff) != (expected & 0xff):
            return False
    
    # Round 3: bytes 32-43
    key3_a = 0xff64a39c4c96443e1b4a7098
    key3_b = 0xcc00fcaa7ca62061717a48e5
    
    for i in range(12):
        byte_val = flag_bytes[32 + i]
        key_byte_a = (key3_a >> (8 * (11 - i))) & 0xff
        key_byte_b = (key3_b >> (8 * (11 - i))) & 0xff
        expected = key_byte_a ^ key_byte_b
        if byte_val != expected:
            return False
    
    # Final check
    checksum = (flag_bytes[15] + flag_bytes[10]) + flag_bytes[4]
    return (checksum & 0xffff) == 0x104

def find_flag():
    flag = [0] * 44
    
    # Round 1
    key1_a = 0xa8b576e88daae1c2885f77f57702fa15
    key1_b = 0xc5d71484f8cf9bf4b76f47904730804b
    for i in range(16):
        key_byte_a = (key1_a >> (8 * (15 - i))) & 0xff
        key_byte_b = (key1_b >> (8 * (15 - i))) & 0xff
        flag[i] = ((key_byte_a - 1) ^ key_byte_b) & 0xff
    
    # Round 2
    key2_a = 0x10659bdc6368e83dd4d62a13f3523aa1
    key2_b = 0x9e3225a9f133b5dea168f4e2851f072f
    for i in range(16):
        key_byte_a = (key2_a >> (8 * (15 - i))) & 0xff
        key_byte_b = (key2_b >> (8 * (15 - i))) & 0xff
        flag[16 + i] = (key_byte_a - key_byte_b) & 0xff
    
    # Round 3
    key3_a = 0xff64a39c4c96443e1b4a7098
    key3_b = 0xcc00fcaa7ca62061717a48e5
    for i in range(12):
        key_byte_a = (key3_a >> (8 * (11 - i))) & 0xff
        key_byte_b = (key3_b >> (8 * (11 - i))) & 0xff
        flag[32 + i] = key_byte_a ^ key_byte_b
    
    return bytes(flag)

flag = find_flag()
print(flag)