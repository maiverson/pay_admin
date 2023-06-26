from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# db.create_all(app=app)

from app.views.api_v1 import api_v1
from app.views.api_v2 import api_v2
from app.views.order_api import order
from app.views.userapi import user

app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_blueprint(api_v2, url_prefix='/api/v2')
app.register_blueprint(order, url_prefix='/api/order')
app.register_blueprint(user, url_prefix='/api/user')