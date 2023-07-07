from app import db
from sqlalchemy_serializer import SerializerMixin
import datetime
from werkzeug.security import generate_password_hash,check_password_hash#转换密码用到的库


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    avatar = db.Column(db.String(150),default='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80')
    roles = db.Column(db.String(500), unique=False)



class User(db.Model,SerializerMixin):
    serialize_rules = ('-children','-password_hash')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(20))
    password_hash = db.Column(db.String(255))
    certno = db.Column(db.String(20))
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_name = db.Column(db.String(50))
    userType = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    userTypeName = db.Column(db.String(20), db.ForeignKey('user_type.typename'))
    children = db.relationship('User', backref=db.backref('parent', remote_side=[id]))
    # rate = db.relationship('Rate', backref=db.backref('rate'))
    baserate = db.Column(db.Float, default=0.48)
    pid = db.Column(db.String(50))
    time = db.Column(db.DateTime,default=datetime.datetime.now())
    totalIncome = db.Column(db.Float,default=0.0)
    balance = db.Column(db.Float,default=0.0)
    status = db.Column(db.Integer, default=1)#1、可用0、不可用2、待定



    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)




class Orders(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(50))
    performance = db.Column(db.Float, default=0.0)
    ChannelTradeNo = db.Column(db.String(50))
    PayPid = db.Column(db.String(20))
    SellerFee = db.Column(db.Float)
    Tid = db.Column(db.Integer)
    time = db.Column(db.DateTime,default=datetime.datetime.now())
    Yifu = db.Column(db.Float)
    Yingfu = db.Column(db.Float)
    income = db.Column(db.Float)



class Income(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    incometype = db.Column(db.Integer)#0、自己 1、团队
    type =  db.Column(db.Integer) #0、收入 1、提现
    income = db.Column(db.Float)#包含提现
    time = db.Column(db.DateTime,default=datetime.datetime.now())#应该和orders 的时间一样


class UserType(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(20),unique=True)

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rate = db.Column(db.Float, default=0.68)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_name = db.Column(db.String(50))
    username = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    userType = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    userTypeName = db.Column(db.String(20), db.ForeignKey('user_type.typename'))
    ali_id = db.Column(db.String(50))
    rate = db.Column(db.Float, default=0.68)#设置的费率
    total = db.Column(db.Float, default=0.0)#总交易额
    qrcode = db.Column(db.String(200))

class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.Integer)# 0、申请 1，同意2、拒绝
    reason = db.Column(db.String(50))
    time = db.Column(db.Time,default=datetime.datetime.now())



#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(80), unique=False)
#     email = db.Column(db.String(120), unique=True)
#     avatar = db.Column(db.String(500), unique=False)
#     roles = db.Column(db.String(500), unique=False)
#     fatherid = db.Column(db.String(80))
#     usertype = db.Column(db.Integer)
#     rate = db.Column(db.Float)

    #
    #
    # def __repr__(self):
    #     return '<User %r>' % self.username

# class Relation(db.Model):
#     __tablename__='relations'
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.String(80))
#     fatherid = db.Column(db.String(80))
#     sonid = db.Column(db.String(80))
#
# class Orders(db.Model):
#     __tablename__='orders'
#     id = db.Column(db.Integer, primary_key=True)
#     payid = db.Column(db.String(80))
#     ChannelTradeNo = db.Column(db.String(80))
#     Tid = db.Column(db.Integer)
#     TotalFee = db.Column(db.Float)
#     UserId = db.Column(db.Integer)
#     Time = db.Column(db.Time)






#
# class Role(db.Model,SerializerMixin):
#     __tablename__='roles'
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(64),unique=True)
#     # users=db.relationship('Users',backref='role')#注意这里用的是role
#
#     def __repr__(self):
#         return '<role %r>'% self.users
#
# class Users(db.Model,SerializerMixin):
#     serialize_rules = ('-role',)
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True,index=True)
#     role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<Users %r>' % self.username
#
# class Merchant(db.Model,SerializerMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     shopName = db.Column(db.String(120))
#     shopAddress = db.Column(db.String(200))
#     lat = db.Column(db.String(80))
#     lnt = db.Column(db.String(80))
#     avatar = db.Column(db.String(200))
#     phone = db.Column(db.String(200))
#     des = db.Column(db.String(1000))
#     status = db.Column(db.Integer)
#     users = db.relationship('ClientUser', backref='merchant')
#     product = db.relationship('Product', backref='merchant')
#
# class ClientUser(db.Model,SerializerMixin):
#     __tablename__ = 'clientuser'
#     serialize_rules = ('-merchant','-orders','-cart','-address')
#     id = db.Column(db.Integer,primary_key=True)
#     userName = db.Column(db.String(80))
#     password = db.Column(db.String(120))
#     avatar = db.Column(db.String(200))
#     phone = db.Column(db.String(200))
#     role = db.Column(db.String(80))
#     status = db.Column(db.Integer)
#     shop_id = db.Column(db.Integer,db.ForeignKey('merchant.id'))
#     orders = db.relationship('Orders', backref='user')
#     cart = db.relationship('Cart', backref='user')
#     address = db.relationship('Address', backref='user')
#
#
#
#
#
#
# class Product(db.Model,SerializerMixin):
#     serialize_rules = ('-merchant',)
#     id = db.Column(db.Integer, primary_key=True)
#     productName = db.Column(db.String(120))
#     price = db.Column(db.String(200))
#     des = db.Column(db.String(1000))
#     store = db.Column(db.Integer)
#     status = db.Column(db.Integer) # 1:正常  0： 下架
#     shop_id = db.Column(db.Integer,db.ForeignKey('merchant.id'))
#     productimage = db.relationship('ProductImage', backref='product')
#     cart = db.relationship('Cart', backref='product')
#     order = db.relationship('Orders', backref='product')
#
# class ProductImage(db.Model,SerializerMixin):
#     serialize_rules = ('-product',)
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
#     imgUrl = db.Column(db.String(120))
#
#
# class Orders(db.Model,SerializerMixin):
#     serialize_rules = ('-product','-user')
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('clientuser.id'))
#     product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
#     num = db.Column(db.Integer)
#     total = db.Column(db.Float)
#     status = db.Column(db.Integer)
#
#
# class Cart(db.Model,SerializerMixin):
#     serialize_rules = ('-product','-user',)
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('clientuser.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     num = db.Column(db.Integer)
#
# class Address(db.Model,SerializerMixin):
#     serialize_rules = ('-user',)
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('clientuser.id'))
#     name = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     address = db.Column(db.String(200))
#
# class Payment(db.Model,SerializerMixin):
#     serialize_rules = ('-order',)
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
#     payType = db.Column(db.Integer)
#     payMoney = db.Column(db.Float)
#
