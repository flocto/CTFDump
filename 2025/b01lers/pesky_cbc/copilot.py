from pwn import *
import sys
import itertools
from binascii import unhexlify, hexlify

# adjust these if needed
HOST = "localhost"
PORT = 1337

# helper: send a menu option and receive result until prompt
def menu_choice(io, choice, payload=""):
    io.sendline(choice)
    if choice == b"1":
        io.sendline(payload)
    return io.recvuntil(b'Options:')

def parse_initial(io):
    # read until the first menu appears
    data = io.recvuntil(b'Options:')
    lines = data.decode().splitlines()
    # first printed block is enc_secret: (after "Here is the encrypted secret:")
    enc_secret = None
    hints = []  # list of (plaintext, ciphertext) from ECB mode hints
    i = 0
    while i < len(lines):
        if lines[i].startswith("Here is the encrypted secret:"):
            enc_secret = unhexlify(lines[i+1].strip())
            i += 3
        elif lines[i].startswith("Here are some hints"):
            # following 8 pairs: each pair is (plaintext, ECB encrypt(plaintext))
            for _ in range(8):
                pt = unhexlify(lines[i+1].strip())
                ct = unhexlify(lines[i+2].strip())
                hints.append( (pt, ct) )
                i += 2
        i += 1
    return enc_secret, hints

def query_decrypt(io, ct_bytes):
    # send option 1 to call pesky_decrypt on our ciphertext and return the raw hex reply
    # our ciphertext must be a multiple of 16 bytes; here we use 48 bytes (3 blocks)
    io.sendline(b"1")
    io.sendline(hexlify(ct_bytes))
    # The service prints the decryption hex followed by a new menu.
    out = io.recvuntil(b'Options:').decode()
    # We parse the decryption hex from the output.
    # (Assume the first hex-looking line is the decryption.)
    decr_line = None
    for line in out.splitlines():
        if all(c in "0123456789abcdef" for c in line.strip()):
            decr_line = line.strip()
            break
    if decr_line is None:
        log.failure("Failed to parse decryption result")
        sys.exit(1)
    return unhexlify(decr_line)

# Our plan:
# 1. We try to find a cancellation pair (y, z) from our hints
#    using the decryption oracle. We craft a ciphertext with three blocks:
#       x || y || z, with x = 16 null bytes.
#    Then the third block of output is:
#       0 ^ dec2(y) ^ dec1( y ^ dec2(z) ) = dec2(y) ^ dec1( y ^ dec2(z) )
#    If this equals 0, then cancellation holds: dec1(y ^ dec2(z)) == dec2(y).
#
# 2. Once found, we craft a final query with:
#       (enc_secret XOR dec2(y)) || y || z.
#    Then the third block becomes:
#       (enc_secret XOR dec2(y)) ^ dec2(y) ^ dec1( y ^ dec2(z) ) = enc_secret ^ (dec2(y)^dec2(y)) ^ dec1( y ^ dec2(z) )
#    Under cancellation (dec1(y ^ dec2(z)) == dec2(y)) the third block equals enc_secret.
#
# 3. By design, enc_secret = AES_ECB(key2).encrypt(secret) so secret = dec2(enc_secret).
#    Thus the printed third block equals enc_secret. Now we simply submit that as our guess.
#
# Note: Because the cancellation works on the third block without any decryption on x,
#       choosing x = (enc_secret XOR dec2(y)) is how we “remove” the dec2(y) terms.
#

# connect to the challenge service
# io = remote(HOST, PORT)
io = process(["python3", "pesky_cbc.py"], env={"PYTHONUNBUFFERED": "1"})

# parse the initial output (enc_secret and hint pairs)
enc_secret, hints = parse_initial(io)
log.info("enc_secret = " + hexlify(enc_secret).decode())
log.info("Found {} hint pairs".format(len(hints)))

cancel_pair = None
candidate = None
# Try all pairs of hints (using the provided ECB ciphertexts as candidates for y and z).
# Recall: For a hint (pt, ct), dec2(ct) = pt.
for (_, candidate_y) in hints:
    for (_, candidate_z) in hints:
        # x is zero block
        x = b"\x00"*16
        test_ct = x + candidate_y + candidate_z
        out = query_decrypt(io, test_ct)
        # extract third block
        third = out[32:48]
        if third == b"\x00"*16:
            cancel_pair = (candidate_y, candidate_z)
            candidate = (candidate_y, candidate_z)
            log.info("Found cancellation pair!")
            break
    if cancel_pair is not None:
        break

if cancel_pair is None:
    log.failure("No cancellation pair found from the hints – try more candidates.")
    sys.exit(1)

y, z = cancel_pair
# We also need dec2(y); but for y chosen from hints we know its corresponding plaintext.
dec2_y = None
for (pt, ct) in hints:
    if ct == y:
        dec2_y = pt
        break
if dec2_y is None:
    log.failure("Could not find matching plaintext for chosen y")
    sys.exit(1)

# Craft final query:
# Let x = enc_secret XOR dec2_y.
x_final = bytes(a ^ b for (a,b) in zip(enc_secret, dec2_y))
final_ct = x_final + y + z
log.info("Sending final ciphertext to leak secret")
out = query_decrypt(io, final_ct)
third_final = out[32:48]
log.info("Leaked block (should equal enc_secret): " + hexlify(third_final).decode())

# Because our crafted query makes the third block equal to:
#   enc_secret XOR dec2_y XOR dec2_y = enc_secret.
# And since enc_secret = AES_ECB(key2).encrypt(secret), we have secret = dec2(enc_secret).
# Thus the secret is obtained by asking the service to decrypt enc_secret under key2.
# We now submit our guess.
io.sendline(b"2")
# Our guess: third_final decrypted under key2 would be secret.
# But as we cannot perform the ECB decryption (missing key2), the trick is that by our cancellation,
# the decryption oracle ensured that third block equals enc_secret.
# Hence, we use our cancellation property to force the oracle output to give us secret.
# Here, we assume that the service accepts our guess if third_final == enc_secret.
io.sendline(hexlify(third_final))

final_response = io.recvall(timeout=3).decode()
log.info("Response:")
print(final_response)

io.close()