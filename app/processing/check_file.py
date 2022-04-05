import numpy as np
from app.processing.MFCC import mfcc
from app.processing.CQCCv2 import cqcc
from app.processing.preprocessing import preprocess
from sklearn.preprocessing import MinMaxScaler
from app import model


def extract(filename, index='single'):
    sig, fs = preprocess(filename)
    fmax = fs / 2
    fmin = fmax / 2 ** 9

    # Установка неоходимых параметров
    B = 84  # number of bins per octave [default = 96]
    d = 12  #

    # CQCC
    cqcc_cof = cqcc(x=sig, fs=fs, B=B, d=d)[:, :B]
    scaler = MinMaxScaler()
    scaler.fit(cqcc_cof)
    cqcc_cof = scaler.transform(cqcc_cof)

    # MFCC
    mfcc_cof = mfcc(fs=fs, sig=sig, fmax=fmax, fmin=fmin)
    scaler1 = MinMaxScaler()
    scaler1.fit(mfcc_cof)
    mfcc_cof = scaler1.transform(mfcc_cof)

    # Объединение коэффициентов
    all_coeff = np.array([np.hstack((cqcc_cof, mfcc_cof))])
    all_coeff = all_coeff.reshape((all_coeff.shape[0], all_coeff.shape[1],all_coeff.shape[2], 1))

    if index == 'single':
        all_coeff = np.array([np.hstack((cqcc_cof, mfcc_cof))])
        all_coeff = all_coeff.reshape((all_coeff.shape[0], all_coeff.shape[1], all_coeff.shape[2], 1))
    elif index == 'multiple':
        all_coeff = np.array(np.hstack((cqcc_cof, mfcc_cof)))
        all_coeff = all_coeff.reshape((all_coeff.shape[0], all_coeff.shape[1], 1))
    return all_coeff


def check(file):
    return model.predict(extract(file))
