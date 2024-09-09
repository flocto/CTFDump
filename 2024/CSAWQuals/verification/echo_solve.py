import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

sample_rate, samples = scipy.io.wavfile.read("out.wav")

print(len(samples), divmod(len(samples), 256))

samples = samples[:-14] # truncate the last 14 samples

def decode(data_with_watermark: np.ndarray, watermark_length: int):
    d0 = 50  # Delay rate
    d1 = 57  # Delay rate for bit
    # alpha = 0.5  # Echo amplitude
    # L = 8 * 1024  # Length of frames
    L = round(0.35 * sample_rate)
    N = int(np.floor(len(data_with_watermark) / L))
    # print(N)
    xsig = np.reshape(np.transpose(data_with_watermark[0:N * L]), (L, N), order='F')
    data = np.empty(N)

    for k in range(N):
        rceps = ifft(np.log(np.abs(fft(xsig[:, k]))))
        # print(len(rceps))
        if rceps[d0] >= rceps[d1]:
            data[k] = 0
        else:
            data[k] = 1

    return np.asarray(data, dtype=np.int16)[:watermark_length]

dec = decode(samples, 256)
dec = int(''.join(map(str, dec)), 2).to_bytes(32, 'big').decode()
print(dec)

# L = round(0.35 * sample_rate)
# N = int(np.floor(len(samples) / L))
# print(N)
# xsig = np.reshape(np.transpose(samples[0:N * L]), (L, N), order='F')
# data = np.empty(N)

# byt = []
# known = '0110001101110011011000010111011101100011011101000110011001111011' # csawctf{
# for k in range(len(known)):
#     rceps = ifft(np.log(np.abs(fft(xsig[:, k]))))
#     byt.append(rceps)

# rang = 16800
# for d0 in range(50, rang):
#     for d1 in range(50, rang):
#         if d0 == d1: 
#             continue
        
#         bits = decode(samples, 256, d0, d1)
#         msg = int(''.join(map(str, bits)), 2).to_bytes(32, 'big').decode()
#         print(d0, d1, bits, msg)
    