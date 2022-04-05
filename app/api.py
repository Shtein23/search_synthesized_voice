from flask import render_template
from app import app, db
from app.models_db import User, History, Setting


@app.route('/api/', methods=['POST', 'GET'])
def api():

    return render_template('404.html')