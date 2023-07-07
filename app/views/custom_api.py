from flask import Blueprint, jsonify, request
from app.models.user import User,Orders,Rate,AdminUser,Income,UserType,Client
from app.models.order import Order
from app import db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import CORS,cross_origin
import requests
import json,time
from config import make_response,parseRequest
from sqlalchemy import text


custom = Blueprint('custom', __name__)
cors = CORS(custom)

@custom.route('/login', methods=['GET','POST'])
def login():
    data = parseRequest(request)
    phone = data.get('phone')
    psw = data.get('password')
    user = User.query.filter_by(mobile=phone).first()
    info = ''
    status = 1
    json = ''
    if not user:
        status = 0
        info = '手机号码不正确'
        json = make_response(status,info)

    elif not psw:
        status = 0
        info = '请输入密码'
        json = make_response(status, info)

    elif not user.check_password_hash(psw):
        status = 0
        info = '密码不正确'
        json = make_response(status, info)

    else:
        status = 1
        info = '登录成功'
        token = create_access_token(identity=phone)#{'token':token}
        dict = user.to_dict()
        dict['token'] = token
        json = make_response(status, info,dict)

    return json


@custom.route('/getUserInfo', methods=['GET','POST'])
@jwt_required()
def getUserInfo():
    phone = get_jwt_identity()
    user = User.query.filter_by(mobile=phone).first()
    code = 1
    info = '成功'
    json = ''
    if not user:
        code = 0
        info = '请求失败'
    else:
        code = 1
        json = user.to_dict()

    return make_response(code, info, json)


@custom.route('/editPassWord', methods=['GET','POST'])
@jwt_required()
def editPassWord():
    phone = get_jwt_identity()
    user = User.query.filter_by(mobile=phone).first()
    data = parseRequest(request)
    password = data.get('password')
    code = 1
    info = '成功'
    json = ''
    if len(password) < 6:
        info = '密码不能少于6位'
        code = 0
    if not user:
        code = 0
        info = '没找到此用户'
    else:
        user.password = password
        db.session.commit()
        code = 1
        info = '密码修改成功'

    return make_response(code, info)


 # parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 #    parent_name = db.Column(db.String(50))
 #    username = db.Column(db.String(20))
 #    mobile = db.Column(db.String(20))
 #    userType = db.Column(db.Integer, db.ForeignKey('user_type.id'))
 #    userTypeName = db.Column(db.String(20), db.ForeignKey('user_type.typename'))
 #    ali_id = db.Column(db.String(50))
 #    rate = db.Column(db.Float, default=0.68)#设置的费率
 #    total = db.Column(db.Float)#总交易额
 #    qrcode = db.Column(db.String(200))

@custom.route('/addClientUser', methods=['GET','POST'])
@jwt_required()
def addClientUser():
    phone = get_jwt_identity()
    user = User.query.filter_by(mobile=phone).first()
    # clineid = get_order_code()
    data = parseRequest(request)
    phone = data.get('phone')
    name = data.get('name')
    rate = data.get('rate')

    # qrcode = getQRCode(clineid)

    client = Client( parent_id=user.id, parent_name=user.name, username=name, mobile=phone, userType=3,
                    userTypeName='自用',
                    rate=rate)
    db.session.add(client)
    db.session.commit()

    qrcode = getQRCode(client.id)

    if qrcode == 0:
        code = 0
        info = '二维码创建失败'
    else:
        client.qrcode = qrcode
        db.session.commit()
        code = 1
        info = '商户创建成功'


    return make_response(code, info)




def getQRCode(clientid):
    url =' http://yjtx.0534666.com/Api/Nb/Qrcode?Id='+str(clientid)
    header = {'key':'bmybymmybdybmyyd'}
    resquest = requests.get(url=url,headers =header)
    jsonStr = json.loads(resquest.text)
    print(jsonStr)
    Errcode = jsonStr['Errcode']
    if(Errcode == 0):
        CodeUrlBlue = jsonStr['CodeUrlBlue']
        return CodeUrlBlue
    else:
        return 0


def get_order_code():
    #  年月日时分秒+time.time()的后7位
    clientNO ='DY'+ str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
    return clientNO