def decode_flag():
    # The expected encoded values from the ef array
    ef = [109, 121, 130, 143, 127, 124, 156, 153, 132, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 85, 154, 111, 124, 85, 99, 115, 73, 147, 139, 123, 136, 81, 98, 125, 74, 142, 153, 62, 122, 128, 99, 115, 71, 86, 169]
    
    # The keys used in encoding
    keys = [11, 22, 33, 44]  # key1, key2, key3, key4
    
    # Decode each character
    flag = ""
    for i in range(len(ef)):
        encoded_value = ef[i]
        key_index = i % 4
        key = keys[key_index]
        
        # Reverse the encoding: subtract the key and handle modulo 256
        # Original: (char_code + key) % 256 = encoded_value
        # Reverse: char_code = (encoded_value - key) % 256
        char_code = (encoded_value - key) % 256
        
        # Convert back to character
        flag += chr(char_code)
    
    return flag

def verify_flag(flag):
    # Verify by re-encoding and comparing with expected values
    keys = [11, 22, 33, 44]
    ef = [109, 121, 130, 143, 127, 124, 156, 153, 132, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 85, 154, 111, 124, 85, 99, 115, 73, 147, 139, 123, 136, 81, 98, 125, 74, 142, 153, 62, 122, 128, 99, 115, 71, 86, 169]
    
    result = []
    for i in range(len(flag)):
        char_code = ord(flag[i])
        key = keys[i % 4]
        encoded = (char_code + key) % 256
        result.append(encoded)
    
    return result == ef

if __name__ == "__main__":
    flag = decode_flag()
    print(f"Decoded flag: {flag}")
    
    # Verify the flag
    if verify_flag(flag):
        print("✓ Flag verification successful!")
    else:
        print("✗ Flag verification failed!")