# Is there an Echo?

Note: My writeup for this will be brief to avoid going through the rabbitholes we went down.

Anyway, first thing to do is notice that the last few parts of the wav file seem suspicious. With `strings`, we can see:

```
$ strings istherecho.wav | tail
...
cepstral domain single echo
```

Now, I wasn't sure what this meant, but googling it along with "steganography" led me to [this paper](https://www.sciencedirect.com/science/article/abs/pii/S0165168410003592) paper. This ended up not being useful, but it did tell me that such a steganography technique exists.

Next, I googled "cepstral domain single echo steganography github", and got [this Github file](https://github.com/ktekeli/audio-steganography-algorithms/blob/master/02-Echo-Hiding/01-Echo-Hiding-Single-Kernel/echo_dec.m) as my first result. 

With a bit more OSINT I found a Python implementation of the same algorithm [here](https://github.com/pawel-kaczmarek/The-A-Files/blob/master/TAF/steganography_methods/EchoMethod.py). 
```python
 def decode(self, data_with_watermark: np.ndarray, watermark_length: int) -> List[int]:
        d0 = 150  # Delay rate
        d1 = 200  # Delay rate for bit
        alpha = 0.5  # Echo amplitude
        L = 8 * 1024  # Length of frames
        N = int(np.floor(len(data_with_watermark) / L))
        xsig = np.reshape(np.transpose(data_with_watermark[0:N * L]), (L, N), order='F')
        data = np.empty(N)

        for k in range(N):
            rceps = ifft(np.log(np.abs(fft(xsig[:, k]))))
            if rceps[d0] >= rceps[d1]:
                data[k] = 0
            else:
                data[k] = 1

        return np.asarray(data, dtype=np.int)[:watermark_length]
```

However, the issue now is that we needed to recover the parameters `d0`, `d1`, and `L`, the two delay rates and the length of the frame used in the algorithm.

`L` was easy. In the spectrogram of the wav, we noticed small bars that seemed to appear with an interval of some multiple of 0.35s, so the L value should be approximately 0.35 * the sample rate.

However, for `d0` and `d1`, we resorted to brute forcing until we found a correct combination. We know that `d0` and `d1` must be a valid index of the result of result of `ifft`, which ended up only being 16800, so we brute forced all of them until we found one that just ended up working. See the attached solve script (should be d0 = 50, d1 = 57)