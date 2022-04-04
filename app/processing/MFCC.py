from librosa.core.spectrum import _spectrogram
from librosa import amplitude_to_db, stft
from librosa.feature import mfcc as mf
from librosa.feature import delta
import numpy as np
from spafe.utils.preprocessing import zero_handling
from spafe.utils.cepstral import cms, cmvn, lifter_ceps
from spafe.fbanks.mel_fbanks import mel_filter_banks


def mfcc(sig,
            fs,
            fmin=0,
            fmax=22000,
            win_length=512,
            hop_length=None,
            n_fft=512
            ):

    sig = sig.reshape(sig.shape[0], )

    N_MFCC = 20
    OVERLAP = False
    MFCC_WIN_LENGTH = 512
    N_MELFILTERS = 40
    use_energy = False
    lifter = 22
    normalize = 1

    if n_fft == None:
        n_fft = win_length

    if hop_length == None:
        if OVERLAP:
            hop_length = int(win_length / 4)
        else:
            hop_length = win_length

    # power spectrum
    D = np.abs(stft(sig, n_fft=n_fft, hop_length=hop_length)) ** 2


    # mel spectrogram
    S1, n_fft1 = _spectrogram(
        S=D,
        n_fft=2048,
        hop_length=256,
        power=2.0,
        win_length=None,
        window="hann",
        center=True,
        pad_mode="reflect"
    )

    # Build a Mel filter
    # mel_basis = filters.mel(sr=rate, n_fft=n_fft1, htk=True)

    scale = "constant"

    imel_fbanks_mat = mel_filter_banks(nfilts=64,
                                               nfft=n_fft1,
                                               fs=fs,
                                               low_freq=fmin,
                                               high_freq=fmax,
                                               scale=scale)
    S_dot = np.dot(imel_fbanks_mat, S1)


    S_nozero = zero_handling(S_dot)
    S_notdb = np.log(S_nozero)
    S = amplitude_to_db(S_notdb)


    MFCC = mf(S=S, n_mfcc=N_MFCC, n_mels=N_MELFILTERS)
    # + 1e-8
    MFCC = MFCC[1:, :]  # exclude 0th mcep


    # liftering
    if lifter > 0:
        MFCC = lifter_ceps(MFCC, lifter)

    # normalization
    if normalize:
        MFCC = cmvn(cms(MFCC))

    MFCC_D = delta(MFCC, order=1)
    MFCC_DD = delta(MFCC, order=2)

    return np.vstack((MFCC, MFCC_D, MFCC_DD)).T




