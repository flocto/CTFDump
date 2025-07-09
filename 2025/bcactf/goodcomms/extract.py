import ggwave
import wave

instance = ggwave.init()

# Open the WAV file for reading
wav_file = wave.open('extract.wav', 'rb')
wav_data = wav_file.readframes(wav_file.getnframes())

res = ggwave.decode(instance, wav_data)
if res is None:
    print("No data found in the WAV file.")

wav_file.close()