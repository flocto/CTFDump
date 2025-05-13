import numpy as np
from typing import List, Tuple

class Midori64Attack:
    def __init__(self):
        # Midori64 S-box
        self.sbox = [
            0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7,
            0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6
        ]
        
        # Inverse S-box
        self.inv_sbox = [0] * 16
        for i in range(16):
            self.inv_sbox[self.sbox[i]] = i
            
        # The nonlinear invariant function g for the S-box
        # g(x) = x[0] ⊕ x[1] ⊕ (x[2] ∧ x[3]) ⊕ x[2]
        
    def bit(self, x: int, pos: int) -> int:
        """Extract a bit at position pos from x."""
        return (x >> pos) & 1
        
    def evaluate_g_nibble(self, x: int) -> int:
        """Evaluate the nonlinear invariant function g on a 4-bit value."""
        bit0 = self.bit(x, 0)
        bit1 = self.bit(x, 1)
        bit2 = self.bit(x, 2)
        bit3 = self.bit(x, 3)
        
        return bit0 ^ bit1 ^ (bit2 & bit3) ^ bit2
    
    def evaluate_g(self, state: bytes) -> int:
        """Evaluate g on the full 64-bit state."""
        result = 0
        for byte_idx in range(8):
            # Each byte contains two nibbles
            nibble1 = (state[byte_idx] >> 4) & 0xF
            nibble2 = state[byte_idx] & 0xF
            
            result ^= self.evaluate_g_nibble(nibble1)
            result ^= self.evaluate_g_nibble(nibble2)
            
        return result
    
    def verify_nonlinear_invariant(self) -> bool:
        """Verify that the nonlinear invariant property holds for the S-box."""
        for x in range(16):
            y = self.sbox[x]
            g_x = self.evaluate_g_nibble(x)
            g_y = self.evaluate_g_nibble(y)
            
            # For Midori64, g(x) = g(S(x)) should hold
            if g_x != g_y:
                return False
                
        return True
    
    def recover_plaintext_bits(self, ciphertexts: List[bytes]) -> bytes:
        """
        Recover 32 bits of plaintext (2 bits from each nibble) using the
        ciphertext-only message recovery attack.
        
        In CBC mode, we have P_i = D(C_i) ⊕ C_{i-1}
        """
        if len(ciphertexts) < 33:
            raise ValueError("Need at least 33 ciphertexts (blocks) for recovery")
            
        # Each block is 8 bytes (64 bits)
        block_size = 8
        
        # We'll recover 2 bits from each of the 16 nibbles = 32 bits
        # These correspond to the bits that are involved in the nonlinear term
        recovered_bits = bytearray(block_size)
        
        # For each of the 16 nibbles, solve a system of linear equations
        for nibble_idx in range(16):
            byte_idx = nibble_idx // 2
            is_high_nibble = (nibble_idx % 2) == 0
            
            # Build the system of linear equations
            equations = []
            results = []
            
            # We need h+1 ciphertexts where h is the number of bits to recover
            # Here, we need 32+1 = 33 ciphertexts
            for i in range(1, 33):
                # Get the relevant parts of the ciphertexts
                c_prev = ciphertexts[i-1][byte_idx]
                c_curr = ciphertexts[i][byte_idx]
                
                # Extract the relevant nibble
                if is_high_nibble:
                    c_prev_nibble = (c_prev >> 4) & 0xF
                    c_curr_nibble = (c_curr >> 4) & 0xF
                else:
                    c_prev_nibble = c_prev & 0xF
                    c_curr_nibble = c_curr & 0xF
                
                # Calculate g(C_{i-1}) ⊕ g(C_i)
                g_prev = self.evaluate_g_nibble(c_prev_nibble)
                g_curr = self.evaluate_g_nibble(c_curr_nibble)
                
                # The result is the constant that will be used in the equation
                result = g_prev ^ g_curr
                
                # The coefficients for the two unknowns (bits 2 and 3)
                # Refer to the equation in the paper:
                # f(x ⊕ u_i) ⊕ f(x ⊕ u_j) = ℓ(u_i ⊕ u_j) ⊕ g(C_i) ⊕ g(C_j)
                # where f is the nonlinear part and ℓ is the linear part of g
                
                # The nonlinear part contributes:
                # (x[2] ⊕ c_prev_nibble[2]) & (x[3] ⊕ c_prev_nibble[3]) ⊕
                # (x[2] ⊕ c_curr_nibble[2]) & (x[3] ⊕ c_curr_nibble[3])
                
                # This gives us our coefficients (derived from the expansion)
                c1 = (self.bit(c_prev_nibble, 3) ^ self.bit(c_curr_nibble, 3)) & 1
                c2 = (self.bit(c_prev_nibble, 2) ^ self.bit(c_curr_nibble, 2)) & 1
                
                equations.append([c1, c2])
                results.append(result)
            
            # Solve the system of equations using Gaussian elimination
            unknown_bits = self._solve_linear_system(equations, results)
            
            # Store the recovered bits
            if is_high_nibble:
                recovered_bits[byte_idx] = (unknown_bits[0] << 7) | (unknown_bits[1] << 6)
            else:
                recovered_bits[byte_idx] |= (unknown_bits[0] << 3) | (unknown_bits[1] << 2)
                
        return recovered_bits
    
    def _solve_linear_system(self, equations: List[List[int]], results: List[int]) -> List[int]:
        """
        Solve a system of linear equations over GF(2) using Gaussian elimination.
        Returns the values of the unknowns.
        """
        n = len(equations[0])  # Number of unknowns
        m = len(equations)     # Number of equations
        
        # Convert to numpy arrays for easier manipulation
        A = np.array(equations, dtype=np.uint8)
        b = np.array(results, dtype=np.uint8)
        
        # Gaussian elimination
        for i in range(min(n, m)):
            # Find pivot
            pivot_row = -1
            for j in range(i, m):
                if A[j, i] == 1:
                    pivot_row = j
                    break
            
            if pivot_row == -1:
                continue  # No pivot found, skip this column
            
            # Swap rows
            if pivot_row != i:
                A[[i, pivot_row]] = A[[pivot_row, i]]
                b[i], b[pivot_row] = b[pivot_row], b[i]
            
            # Eliminate other rows
            for j in range(m):
                if j != i and A[j, i] == 1:
                    A[j] ^= A[i]  # XOR operation (addition in GF(2))
                    b[j] ^= b[i]
        
        # Back substitution
        x = np.zeros(n, dtype=np.uint8)
        for i in range(n-1, -1, -1):
            # Check if this variable is determined
            if np.sum(A[:, i]) == 1:
                row_idx = np.argmax(A[:, i])
                # Calculate value using other variables
                val = b[row_idx]
                for j in range(i+1, n):
                    val ^= (A[row_idx, j] & x[j])
                x[i] = val
        
        return x.tolist()

# Example usage
def main():
    attack = Midori64Attack()
    
    # Verify that the nonlinear invariant property holds for the S-box
    if attack.verify_nonlinear_invariant():
        print("Nonlinear invariant property holds for the Midori64 S-box!")
    else:
        print("Nonlinear invariant property does not hold for the Midori64 S-box.")
        return
    
    ct = open('ct1.bin', 'rb').read()
    ciphertexts = [ct[i:i+8] for i in range(0, len(ct), 8)]
    # Recover the plaintext bits
    try:
        recovered_bits = attack.recover_plaintext_bits(ciphertexts)
        print("Recovered 32 bits of plaintext:")
        print(' '.join(f'{b:08b}' for b in recovered_bits))
    except Exception as e:
        print(f"Error during plaintext recovery: {e}")

if __name__ == "__main__":
    main()