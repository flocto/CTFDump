# from z3 import *
from cvc5.pythonic import *
from dist import encrypt, rot, round_constants, M


def test_recover_flag():
    # Known values
    p1 = b'please like and subscribe!!!!!!!'
    p1_int = int.from_bytes(p1, 'big')
    
    # These are the output values from dist.py (replace with actual values)
    c1 = 75041939973389574321824911996962649664303372791392596052720514831677089270984
    c2 = 43874176852610031103309995367328596091907619633676518750651598946069344089287
    
    # Create a Z3 solver
    s = Solver()
    
    # Create a BitVec for the key (256 bits)
    key = BitVec('key', 256)
    
    # Define the rotation function for Z3
    def z3_rot(n, r):
        # return LShR(n, r) | ((n << (256 - r)) & (2**256 - 1))
        return RotateRight(n, r)
    
    # Define the encryption function in Z3 terms
    def z3_encrypt(k, b):
        result = b
        for i in range(24):
            result = (result + k)
            result = z3_rot(result, round_constants[i])
        return result
    
    
    # Add constraint: encrypt(key, p1) == c1
    s.add(z3_encrypt(key, p1_int) == c1)
    
    # Check if the model is satisfiable
    if s.check() == sat:
        model = s.model()
        recovered_key = model[key].as_long()
        
        # Now decrypt c2 to get the flag
        # For this simple cipher, we need to work backwards through the rounds
        # This is complex for this cipher, so we'll just check that using the key for encryption works
        
        # Get the decrypted flag
        flag_int = decrypt_message(recovered_key, c2)
        flag = int_to_bytes(flag_int)
        
        print(f"Recovered flag: {flag}")
    else:
        print("No solution found for the key.")
        return None

def inv_rot

def decrypt_message(key, ciphertext):
    