import math
from fractions import Fraction
import gmpy2

def parse_ciphertext():
    """Parse the RSA parameters from ciphertext.txt"""
    with open('ciphertext.txt', 'r') as f:
        content = f.read()
    
    # Extract ct, e, N values
    lines = content.strip().split('\n')
    ct = int(lines[0].split('=')[1].strip())
    e = int(lines[1].split('=')[1].strip())
    N = int(lines[2].split('=')[1].strip())
    
    return ct, e, N

def continued_fraction(n, d):
    """Generate continued fraction representation of n/d"""
    cf = []
    while d != 0:
        q = n // d
        cf.append(q)
        n, d = d, n - q * d
    return cf

def convergents(cf):
    """Generate convergents from continued fraction"""
    convergents = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    
    for a in cf:
        h_next = a * h_curr + h_prev
        k_next = a * k_curr + k_prev
        convergents.append((h_next, k_next))
        h_prev, h_curr = h_curr, h_next
        k_prev, k_curr = k_curr, k_next
    
    return convergents

def wiener_attack(e, N):
    """Implement Wiener's attack to find small private key d"""
    # Generate continued fraction of e/N
    cf = continued_fraction(e, N)
    convs = convergents(cf)
    
    for k, d in convs:
        if k == 0:
            continue
            
        # Check if this convergent gives us the correct d
        # For RSA: ed ≡ 1 (mod φ(N))
        # So ed - 1 should be divisible by φ(N)
        
        if (e * d - 1) % k == 0:
            phi_candidate = (e * d - 1) // k
            
            # For N = pq, φ(N) = (p-1)(q-1) = N - p - q + 1
            # So p + q = N - φ(N) + 1
            s = N - phi_candidate + 1
            
            # Solve quadratic: x² - sx + N = 0
            discriminant = s * s - 4 * N
            
            if discriminant >= 0:
                # sqrt_disc = int(math.sqrt(discriminant))
                sqrt_disc = gmpy2.isqrt(discriminant)
                if sqrt_disc * sqrt_disc == discriminant:
                    p = (s + sqrt_disc) // 2
                    q = (s - sqrt_disc) // 2
                    
                    if p * q == N and p > 1 and q > 1:
                        return d, p, q
    
    return None, None, None

def decrypt_rsa(ct, d, N):
    """Decrypt RSA ciphertext using private key d"""
    return pow(ct, d, N)

def int_to_bytes(n):
    """Convert integer to bytes"""
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, 'big')

def main():
    # Parse the challenge data
    ct, e, N = parse_ciphertext()
    
    print(f"Ciphertext: {ct}")
    print(f"Public exponent e: {e}")
    print(f"Modulus N: {N}")
    print(f"e bit length: {e.bit_length()}")
    print(f"N bit length: {N.bit_length()}")
    
    # Perform Wiener's attack
    print("\nPerforming Wiener's attack...")
    d, p, q = wiener_attack(e, N)
    
    if d is None:
        print("Wiener's attack failed!")
        return
    
    print(f"Found private key d: {d}")
    print(f"Found prime p: {p}")
    print(f"Found prime q: {q}")
    print(f"Verification: p * q = {p * q == N}")
    
    # Decrypt the ciphertext
    plaintext_int = decrypt_rsa(ct, d, N)
    print(f"Decrypted integer: {plaintext_int}")
    
    # Convert to bytes and extract flag
    try:
        plaintext_bytes = int_to_bytes(plaintext_int)
        plaintext_str = plaintext_bytes.decode('utf-8', errors='ignore')
        print(f"Decrypted message: {plaintext_str}")
        
        # Look for flag format
        if 'bcactf{' in plaintext_str:
            flag_start = plaintext_str.find('bcactf{')
            flag_end = plaintext_str.find('}', flag_start) + 1
            flag = plaintext_str[flag_start:flag_end]
            print(f"\nFLAG: {flag}")
        else:
            print(f"Raw bytes: {plaintext_bytes}")
            
    except Exception as e:
        print(f"Error decoding: {e}")
        print(f"Raw integer: {plaintext_int}")

if __name__ == "__main__":
    main()