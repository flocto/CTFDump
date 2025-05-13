data = open('technically_correct', 'rb').read()

open('tmp.bin', 'wb').write(data[1:])