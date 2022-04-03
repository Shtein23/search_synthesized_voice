import config
from app import app, model
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
import datetime
import numpy as np


def rd(x, y=0):

    m = int('1' + '0' * y)
    q = x * m
    c = int(q)
    i = int((q - c) * 10)
    if i >= 5:
        c += 1
    return c / m

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


@app.route('/')
@app.route('/index')
def index():
    if request.method == 'GET':
        return render_template('index.html', exmp=os.listdir('wav/example'))

    elif request.method == 'POST':

        if request.form.get('exp'):
            file = 'wav/example/'+str(request.form.get('exp'))
            filename = str(request.form.get('exp'))
        else:
            file = request.files['file']
            print(type(file))
            filename = secure_filename(file.filename)

        tr = 0.1575779914855957
        score = model.predict(extract(file))
        if score[0][0] > tr:
            score_str = 'Естественный'
        else:
            score_str = 'Спуфинг'
        itog = [str(datetime.now()), filename, rd(score[0][0], y=2), score_str]


        render_template('index.html', bd=bd[id], exmp=os.listdir('wav/example'))
    else:
        return redirect('404.html', 404)