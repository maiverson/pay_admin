from app import db
from flask import jsonify
import json
from sqlalchemy_serializer import SerializerMixin

class Order(db.Model):
    order_no = db.Column(db.String(120), primary_key=True)
    price = db.Column(db.Integer, unique=False)
    status = db.Column(db.String(80), unique=False)
    username = db.Column(db.String(120), unique=False)
    timestamp = db.Column(db.String(120), unique=False)

    def __repr__(self):
        return '<Order %r>' % self.username


class DragTable(db.Model,SerializerMixin):
    # serialize_rules = ('-pageviews','-reviewer','-author')
    id = db.Column(db.String(120), primary_key=True)
    author = db.Column(db.String(120), unique=False)
    comment_disabled = db.Column(db.BOOLEAN, unique=False)
    content = db.Column(db.String(500), unique=False)
    content_short = db.Column(db.String(120), unique=False)
    display_time = db.Column(db.String(120), unique=False)
    forecast = db.Column(db.Float, unique=False)
    image_uri = db.Column(db.String(120), unique=False)
    reviewer = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)
    timestamp = db.Column(db.String(120), unique=False)
    title = db.Column(db.String(120), unique=False)
    type = db.Column(db.String(120), unique=False)
    importance = db.Column(db.Integer, unique=False)
    pageviews = db.Column(db.Integer, unique=False)

    #
    # def __repr__(self):
    #     jsonStr = {'id':self.id,
    #                'author':self.author,
    #                'comment_disabled':self.comment_disabled,
    #                'content':self.content,
    #                'content_short': self.content_short,
    #                'display_time':self.display_time,
    #                'forecast': self.forecast,
    #                'image_uri': self.image_uri,
    #                'reviewer': self.reviewer,
    #                'status': self.status,
    #                'timestamp': self.timestamp,
    #                'title': self.title,
    #                'type': self.type,
    #                'importance': self.importance,
    #                'pageviews': self.pageviews,
    #                }
    #
    #     return json.dumps(jsonStr)