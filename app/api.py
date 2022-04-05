from flask import render_template
from app import app, db, model
from app.models_db import User, History, Setting
from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from app.processing.check_file import check
import datetime


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.ALLOWED_EXTENSIONS


def rd(x, y=0):

    m = int('1' + '0' * y)
    q = x * m
    c = int(q)
    i = int((q - c) * 10)
    if i >= 5:
        c += 1
    return c / m


@app.route('/api/', methods=['POST'])
def api():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.args.get('name')).first()
        if user is None or not user.check_password(request.args.get('api_kei')):
            return 'Неправильные данные для доступа к проверке'

        # Получаемм присланный файл на проверку
        if request.files['file'] and allowed_file(request.files['file'].filename):
            file = request.files['file']
            filename = secure_filename(file.filename)

            tr = 0.1575779914855957
            score = check(file)
            score_str = 'Естественный' if score[0][0] > tr else 'Спуфинг'
            h = History(date=datetime.date.today(), file_name=filename, score=rd(score[0][0], y=2),
                        score_str=score_str)
            db.session.add(h)
            db.session.commit()
            return jsonify(
                dict(date=datetime.date.today().strftime('%d.%m.%Y'), file_name=filename, score=rd(score[0][0], y=2),
                     score_str=score_str))
    else:
        return 'Error method'
