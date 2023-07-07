import os
from flask import jsonify

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:haha0^_^0@localhost:3306/linyilife'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'dayeadminkey'
JWT_ACCESS_TOKEN_EXPIRES=3600*24*30


def make_response(status_code, message, data=None):
    response = {
        'code': status_code,
        'message': message,
        'data': data
    }
    return jsonify(response)


def parseRequest(req):
    data = {}
    if req.method == 'GET':
        data = req.args
    elif req.method == 'POST':
        data = req.json
    return data