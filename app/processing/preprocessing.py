import numpy as np
from librosa import load

def preprocess(file, silens_coef=0.025, fs=16000):
    # Децимация - все входные данные идут с 16к дискретизацией
    signal, sr = load(file, mono=True, sr=fs)
    # sr, signal = wavfile.read(file)

    # нормализация сигнала
    signal = np.double(signal)

    signal = signal / (2.0 ** 15)
    DC = signal.mean()
    MAX = (np.abs(signal)).max()
    signal = (signal - DC) / (MAX + 0.0000000001)


    # микширование в моно
    signal = signal.reshape(signal.shape[0], 1)
    # newsignal = signal
    # удаление тишины
    newsignal = np.array(list(filter(lambda x: abs(x) > silens_coef, signal)))


    newsignal = newsignal.reshape(newsignal.shape[0], 1)
    if newsignal.shape[0] < 16321:
        newsignal = np.vstack((newsignal, np.zeros((16321 - newsignal.shape[0], 1))))
    if newsignal.shape[0] > 16321:
        newsignal = newsignal[:16321, :]

    return newsignal, sr

