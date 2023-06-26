from app import app, db
from app.models.user import User
from app.models.order import Order
from flask import jsonify

# db.create_all(app=app)

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
        data = req.form
    return data