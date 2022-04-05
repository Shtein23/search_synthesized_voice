import config
from app import app, db
from app.models_db import User, History, Setting
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
import datetime
from flask import jsonify
from app.processing.check_file import check


def rd(x, y=0):

    m = int('1' + '0' * y)
    q = x * m
    c = int(q)
    i = int((q - c) * 10)
    if i >= 5:
        c += 1
    return c / m


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', exmp=os.listdir('app/wav/example'), history=reversed(History.query.all()))

    elif request.method == 'POST':
        print(request.form.get('name_file'))
        if request.form.get('name_file'):
            file = 'app/wav/example/'+str(request.form.get('name_file'))
            filename = str(request.form.get('name_file'))
        else:
            print(request.files['file'])
            file = request.files['file']
            filename = secure_filename(file.filename)

        tr = 0.1575779914855957
        score = check(file)

        score_str = 'Естественный' if score[0][0] > tr else 'Спуфинг'

        h = History(date=datetime.date.today(), file_name=filename, score=rd(score[0][0], y=2),
                    score_str=score_str)
        db.session.add(h)
        db.session.commit()
        return jsonify(dict(date=datetime.date.today().strftime('%d.%m.%Y'), file_name=filename, score=rd(score[0][0], y=2),
                            score_str=score_str))
    else:
        return redirect('404.html', 404)
