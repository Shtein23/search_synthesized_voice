from librosa import amplitude_to_db, cqt
import numpy as np
import scipy



def cqcc(x, fs, B=84, d=12):
    x = x.reshape(x.shape[0], )

    qtrans = cqt(x, sr=fs, n_bins=B, bins_per_octave=d)

    # get log power Q-spectrogram
    qS = np.abs(qtrans)
    qS = qS ** 2

    # power spectrum of Q-transform
    qspec = amplitude_to_db(qS, amin=1e-10, top_db=80.0).astype('float32')

    # resample
    def resample(s, fs_orig, fs_new, axis=0, best_algorithm=True):
        fs_orig = int(fs_orig)
        fs_new = int(fs_new)
        if fs_orig != fs_new:
            import resampy
            s = resampy.resample(s, sr_orig=fs_orig, sr_new=fs_new, axis=axis,
                                 filter='kaiser_best' if best_algorithm else 'kaiser_fast')
        return s

    res_qspec = resample(qspec, fs, 44000)

    CQcc = scipy.fftpack.dct(res_qspec, type=2, norm='ortho', axis=0)

    return CQcc.T