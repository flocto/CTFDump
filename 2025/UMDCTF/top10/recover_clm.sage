# Requires SageMath environment (https://www.sagemath.org/)

# Define the field GF(2)
F = GF(2)

# Define the polynomial ring over GF(2)
P.<x> = PolynomialRing(F)

# --- Input: The 128-bit result of the forward operation ---
# Use the example output from your assertion
xmm0_reversed_hex = "0E0E84CD0FBAD07BA801DD1AB614E490"

# Convert the reversed hex string (as seen in the assertion)
# back to a little-endian integer value
try:
    xmm0_bytes_big_endian = bytes.fromhex(xmm0_reversed_hex)
    xmm0_bytes_little_endian = xmm0_bytes_big_endian[::-1]
    res_int = Integer(int.from_bytes(xmm0_bytes_little_endian, 'little'))
    print(f"Input Result Integer (little-endian): 0x{res_int.hex()}")
except ValueError:
    print(f"Error: Invalid hexadecimal input string: {xmm0_reversed_hex}")
    # exit() # Or handle error appropriately

# Convert the result integer to a polynomial over GF(2)
# Ensure the integer is treated correctly for polynomial conversion
res_poly = P(res_int.digits(2)) # digits(2) gives coefficients in ascending order of powers
print(f"\nResult Polynomial (res_poly) [Degree: {res_poly.degree()}]:")
# print(res_poly) # Printing can be very long

# --- Inverse Step: Polynomial Factorization ---
print("\nFactoring the result polynomial over GF(2)...")
# This finds the irreducible factors and their multiplicities
# The result is a list of pairs: (irreducible_factor, exponent)
try:
    factors = res_poly.factor()
    print(f"\nIrreducible Factors of res_poly:")
    print(factors)
except Exception as e:
    print(f"\nAn error occurred during factorization: {e}")
    factors = [] # Ensure factors is iterable

# --- Reconstructing Potential Original Pairs ---
print("\n--- Reconstructing Potential (lo_poly, hi_poly) Pairs ---")
print("Need to find pairs of factors (A, B) such that:")
print("1. A * B = res_poly")
print("2. degree(A) <= 63")
print("3. degree(B) <= 63")

# Helper function to get all divisors by combining irreducible factors
def get_divisors(factor_list):
    """ Computes all divisors from a list of (factor, exponent) pairs. """
    divs = {P(1)} # Start with the divisor 1
    for p, e in factor_list:
        new_divs = set()
        # Combine existing divisors with powers of the current factor p^0, p^1, ..., p^e
        for i in range(e + 1):
            factor_power = p**i
            for d in divs:
                new_divs.add(d * factor_power)
        divs = new_divs
    return divs

potential_pairs = []
if factors: # Proceed only if factorization was successful and non-trivial
    all_divisors = get_divisors(factors)
    print(f"\nFound {len(all_divisors)} distinct divisors (potential candidates for one factor).")

    print("Checking divisor pairs against degree constraints (<= 63)...")
    for potential_lo in all_divisors:
        if potential_lo.degree() <= 63:
            # Calculate the corresponding potential_hi using polynomial division
            # quo_rem ensures we only consider exact factors
            potential_hi, remainder = res_poly.quo_rem(potential_lo)

            if remainder == 0 and potential_hi.degree() <= 63:
                # This pair (potential_lo, potential_hi) is a valid candidate
                potential_pairs.append((potential_lo, potential_hi))
                # Optional: Avoid adding swapped pairs (B, A) if (A, B) is already added
                # This check is slightly complex due to needing canonical representation or comparing sets

    print(f"\nFound {len(potential_pairs)} potential (lo_poly, hi_poly) pairs satisfying degree constraints.")

else:
     print("\nFactorization did not yield factors to check.")


# --- Output Potential Pairs ---
if not potential_pairs:
    print("\nNo pairs of factors satisfy the degree constraints (<= 63). Inverse might not exist under these constraints or the input polynomial was trivial/irreducible > degree 63.")
else:
    print("\nPotential (lo_poly, hi_poly) candidate pairs:")
    # Displaying the full polynomials can be verbose, maybe show degrees and hex values
    for i, (p_lo, p_hi) in enumerate(potential_pairs):
        # Convert polynomials back to integers to show potential hex values
        coeffs_lo = p_lo.list()
        coeffs_lo.extend([0] * (64 - len(coeffs_lo))) # Pad to 64 bits
        candidate_lo_int = Integer(coeffs_lo, 2)

        coeffs_hi = p_hi.list()
        coeffs_hi.extend([0] * (64 - len(coeffs_hi))) # Pad to 64 bits
        candidate_hi_int = Integer(coeffs_hi, 2)

        # Construct the potential original xmm4 from this pair
        lo_bytes_cand = int(candidate_lo_int).to_bytes(8, 'little')
        hi_bytes_cand = int(candidate_hi_int).to_bytes(8, 'little')

        if any(x < ord("!") or x > ord("~") for x in lo_bytes_cand):
            continue
        if any(x < ord("!") or x > ord("~") for x in hi_bytes_cand):
            continue

        print(f"\nPair {i+1}:")
        print(f"  Potential lo_poly degree: {p_lo.degree()}")
        print(f"  Potential hi_poly degree: {p_hi.degree()}")
        print(f"  Potential lo_int (hex): 0x{candidate_lo_int.hex().zfill(16)}")
        print(f"  Potential hi_int (hex): 0x{candidate_hi_int.hex().zfill(16)}")
        # print(f"  Potential lo_poly: {p_lo}") # Uncomment to see full polynomial
        # print(f"  Potential hi_poly: {p_hi}") # Uncomment to see full polynomial

       

        xmm4_cand_bytes = lo_bytes_cand + hi_bytes_cand
        print(f"  Potential xmm4 (hex): {xmm4_cand_bytes.hex()}")


print("\n--- Conclusion ---")
print("The inverse operation yields candidate pairs based on polynomial factorization.")
print("If multiple pairs are found, you cannot uniquely determine the original xmm4 from xmm0 alone.")
print("You would need additional information or context to select the correct original pair.")
# For the specific example 0E0E..., factorization should recover the pair corresponding to AAAABBBBCCCCDDDD
# You can manually check if 0x4242424241414141 and 0x4444444443434343 appear in the candidate list.