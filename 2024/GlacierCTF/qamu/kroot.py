challenge = open('challenge', 'rb').read()

challenge += b'\x00' * 0x1004000

open('challenge_padded', 'wb').write(challenge)