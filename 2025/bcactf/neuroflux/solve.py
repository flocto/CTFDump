import hashpumpy
import requests

hsh = '666233353964316162363434636230653962366164333364336461653337303938652236d5'
user = 'admin605158466'

salt_hex = hsh[:34]
original_hash = hsh[34:]
salt_bytes = bytes.fromhex(salt_hex)

for password_length in range(1, 50):
    try:
        new_hash, new_message = hashpumpy.hashpump(
            original_hash,
            b"",
            b"admin",
            len(salt_bytes) + password_length
        )
        
        new_password = new_message[len(salt_bytes):]
        
        response = requests.post('http://challs.bcactf.com:30147/', data={
            'username': user,
            'password': new_password
        })
        
        print(f"{password_length}: {new_password} -> {response.status_code}")
     
            
    except Exception as e:
        print(f"Error with password length {password_length}: {e}")
        continue