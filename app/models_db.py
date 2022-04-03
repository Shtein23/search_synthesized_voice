from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    file_name = db.Column(db.String(64), index=True)
    score = db.Column(db.Float)
    score_str = db.Column(db.String(16))

    def __repr__(self):
        return f'<Дата проверки: {self.date}, Оценка: {self.score_strс}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    api_key_hash = db.Column(db.String(128))


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    value = db.Column(db.String(64))
