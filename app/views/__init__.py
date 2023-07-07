from app import app, db
from app.models.user import User
# from app.models.order import Order
from flask import jsonify

# db.create_all(app=app)

with app.app_context():
    print('shkakfkakfa')
    db.create_all()

def make_response(status_code, message, data=None):
    response = {
        'code': status_code,
        'message': message,
        'data': data
    }
    return jsonify(response)


def parseRequest(req):
    if req.method == 'GET':
        return req.args
    elif req.method == 'POST':
        return req.json
