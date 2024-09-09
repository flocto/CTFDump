import numpy as np
import scipy
import matplotlib.pyplot as plt

sample_rate, samples = scipy.io.wavfile.read("out.wav")

cur = 0
step = round(0.35 * sample_rate)
vari = round(0.05 * sample_rate)

out = []

while cur + step < len(samples):
    l, r = cur, cur
    if cur > 0:
        l = cur - vari
    if cur + step < len(samples):
        r = cur + vari
    
    chunk = samples[l:r]
    out.extend(chunk)
    cur += step

scipy.io.wavfile.write("out2.wav", sample_rate, np.array(out, dtype=np.int16))