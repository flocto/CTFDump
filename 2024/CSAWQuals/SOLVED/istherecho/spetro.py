import numpy as np
import scipy
import matplotlib.pyplot as plt

sample_rate, samples = scipy.io.wavfile.read("out.wav", mmap=True)

cur = 0
step = round(0.35 * sample_rate)
vari = round(0.01 * sample_rate)
i = 0

while cur + step < len(samples):
    i += 1
    cur += step

    chunk = samples[cur - vari:cur + vari]

    fft = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(fft.size, 1/sample_rate)
    freqs = freqs[:len(freqs)//2][1:]
    fft = np.abs(fft)[:len(fft)//2][1:]

    plt.plot(freqs, fft)
    plt.title(f"{round(i * 0.35 - 0.01, 2)} : {round(i * 0.35 + 0.01, 2)}")
    plt.show()
    