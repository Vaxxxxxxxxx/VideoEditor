import librosa
import numpy as np

'''
Adapted from 
https://medium.com/analytics-vidhya/how-to-create-a-music-visualizer-7fad401f5a69 Avi Rzayev
and
McFee, B., Raffel, C., Liang, D., Ellis, D. P., McVicar, M., 
# Battenberg, E., & Nieto, O. (2015, July). librosa: Audio and music 
# signal analysis in python. In Proceedings of the 14th python in
# science conference (Vol. 8, pp. 18-25).
and
https://librosa.org/doc/latest/index.html
'''


class AudioInitializer:
    def __init__(self):
        self.__filename = "../TempFrames/output.mp3"
        # getting information from the file
        self.__y, self.__sr = librosa.load(self.__filename)
        # short-time Fourier transform
        self.__stft = librosa.stft(self.__y, hop_length=512, n_fft=10216)
        # mapping the magnitudes to a decibel scale
        # keep an ordinary (linear) spectrogram
        self.__spectrogram = librosa.amplitude_to_db(np.abs(self.__stft), ref=np.max)
        # getting an array of frequencies
        self.__frequencies = librosa.fft_frequencies(n_fft=10216, sr=self.__sr)
        # getting an array of time periodic
        times = librosa.frames_to_time(np.arange(self.__spectrogram.shape[1]), sr=self.__sr, n_fft=10216)
        # first element divide by last element
        self.__time_index_ratio = len(times) / times[len(times) - 1]
        self.__frequencies_index_ratio = len(self.__frequencies) / self.__frequencies[len(self.__frequencies) - 1]

    def get_decibel(self, target_time, freq):
        return self.__spectrogram[int(freq * self.__frequencies_index_ratio)][
            int(target_time * self.__time_index_ratio)]
