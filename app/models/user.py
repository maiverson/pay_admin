from app import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    avatar = db.Column(db.String(500), unique=False)
    roles = db.Column(db.String(500), unique=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model,SerializerMixin):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    # users=db.relationship('Users',backref='role')#注意这里用的是role

    def __repr__(self):
        return '<role %r>'% self.users

class Users(db.Model,SerializerMixin):
    serialize_rules = ('-role',)
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Users %r>' % self.username

class Merchant(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    shopName = db.Column(db.String(120))
    shopAddress = db.Column(db.String(200))
    lat = db.Column(db.String(80))
    lnt = db.Column(db.String(80))
    avatar = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    des = db.Column(db.String(1000))
    status = db.Column(db.Integer)
    users = db.relationship('ClientUser', backref='merchant')
    product = db.relationship('Product', backref='merchant')

class ClientUser(db.Model,SerializerMixin):
    __tablename__ = 'clientuser'
    serialize_rules = ('-merchant','-orders','-cart','-address')
    id = db.Column(db.Integer,primary_key=True)
    userName = db.Column(db.String(80))
    password = db.Column(db.String(120))
    avatar = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    role = db.Column(db.String(80))
    status = db.Column(db.Integer)
    shop_id = db.Column(db.Integer,db.ForeignKey('merchant.id'))
    orders = db.relationship('Orders', backref='user')
    cart = db.relationship('Cart', backref='user')
    address = db.relationship('Address', backref='user')






class Product(db.Model,SerializerMixin):
    serialize_rules = ('-merchant',)
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(120))
    price = db.Column(db.String(200))
    des = db.Column(db.String(1000))
    store = db.Column(db.Integer)
    status = db.Column(db.Integer) # 1:正常  0： 下架
    shop_id = db.Column(db.Integer,db.ForeignKey('merchant.id'))
    productimage = db.relationship('ProductImage', backref='product')
    cart = db.relationship('Cart', backref='product')
    order = db.relationship('Orders', backref='product')

class ProductImage(db.Model,SerializerMixin):
    serialize_rules = ('-product',)
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    imgUrl = db.Column(db.String(120))


class Orders(db.Model,SerializerMixin):
    serialize_rules = ('-product','-user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('clientuser.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    num = db.Column(db.Integer)
    total = db.Column(db.Float)
    status = db.Column(db.Integer)


class Cart(db.Model,SerializerMixin):
    serialize_rules = ('-product','-user',)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clientuser.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    num = db.Column(db.Integer)

class Address(db.Model,SerializerMixin):
    serialize_rules = ('-user',)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clientuser.id'))
    name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(200))

class Payment(db.Model,SerializerMixin):
    serialize_rules = ('-order',)
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    payType = db.Column(db.Integer)
    payMoney = db.Column(db.Float)

