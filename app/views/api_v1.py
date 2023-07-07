from flask import Blueprint, jsonify, request
from app.models.user import User,Orders,Rate,AdminUser,Income
from app.models.order import Order
from app import db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import CORS,cross_origin
import requests
import json,time
from config import make_response,parseRequest


api_v1 = Blueprint('api_v1', __name__)
cors = CORS(api_v1)

@api_v1.route('/login', methods=['GET','POST'])
def login():
    data = parseRequest(request)
    username = data.get('username')
    psw = data.get('password')
    print(username,psw)
    user = AdminUser.query.filter_by(name=username).first()
    info = ''
    status = 1
    json = ''
    if not user:
        status = 0
        info = '用户名不正确'
        json = make_response(status,info)

    elif psw != user.password:
        status = 0
        info = '密码不正确'
        json = make_response(status, info)

    else:
        status = 1
        info = '登录成功'
        token = create_access_token(identity=username)
        json = make_response(status, info,{'token':token})

    return json

@api_v1.route('/userinfo', methods=['GET','POST'])
@jwt_required()
def get_user_info():
    data = parseRequest(request)
    token = data.get('token')
    username = get_jwt_identity()

    user = AdminUser.query.filter_by(name=username).first()
    print(user)
    code = 1
    info = '成功'
    json = ''
    if not user:
        code = 0
        info = '请求失败'
    else:
        code = 1
        json = {'name': user.name, 'email': user.email,'avatar':user.avatar,'roles':[user.roles]}

    return make_response(code,info,json)

@api_v1.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    #分页查询
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('per_page', 10))
    # users = User.query.limit(per_page).offset((page - 1) * per_page).all()
    # total_count = User.query.count()
    # total_pages = (total_count + per_page - 1) // per_page

    return make_response(200,'success',{'users': [{'username': user.username, 'email': user.email} for user in users]})

@api_v1.route('/adduser', methods=['POST','GET'])
def create_user():
    data = parseRequest(request)
    print(data.get('username'))
    username = data.get('username')
    email = data.get('email')
    psw = data.get('password')
    avatar = data.get('avatar')
    roles = data.get('roles')
    fatherid = data.get('fatherid')
    type = data.get('usertype')
    rate = data.get('rate')

    user = User(username=username, email=email,password=psw,avatar=avatar,roles=roles,fatherid = fatherid,usertype=type,rate=rate)
    db.session.add(user)
    db.session.commit()
    response = {'message': 'User created successfully!'}
    return make_response(200,'success',response)

@api_v1.route('/getuser', methods=['GET'])
def get_user():
    data = parseRequest(request)
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    response = ''
    if not user:
        response = 'User not found'

        return make_response(200,'success',response)
    response = {'username': user.username, 'email': user.email}
    return make_response(200,'success',response)

@api_v1.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    username = request.json.get('username')
    email = request.json.get('email')
    user.username = username
    user.email = email
    user.fatherid = 0
    user.usertype = 1
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

@api_v1.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})


@api_v1.route('/gettestuser', methods=['GET'])
def get_testusers():
    users = Users.query.all()
    roles = Role.query.all()
    print( users)

    rolist = [role.to_dict() for role in roles]
    # print(rolist)
    return make_response(200,'success',rolist)


@api_v1.route('/getData', methods=['GET'])
def get_testData():
    url = 'http://yjtx.0534666.com/Manage/TxTradeList?PageNo=1&PageSize=1000&Status=100'
    headers = {'Cookie':'.AspNet.ApplicationCookie=zCT7fSghWi7Z4HyAQuhVIZ0I833ZLbS9pu71QPiQTQDmDKoVzzFugibdMaQ-AaYnbyAOjDMA8EUxlZG1Z1U-IA7GMbIHjtdExwvGWHio7odV1GhxQOekLHUH_muqdvxB21imnRRiNO2lYa7TYo0G5HWIo2-JIRE_xEL8ar-E9SgkySaI0JPlZL7ym1sRVGdRrWDeD28S4iZsN-x66sstO7FeDyDiyEbi73AA5rURUSgWHK2mvHnBpmidv2ncDsCwvPdVTRnewRVGUckVCbjbpwBinH5bt9TnLTNyfabtzqOjWCFBrpgVskjrig9__-593emVSbm3SD2dT2mfIBuEzA'}
    response = requests.get(url=url,headers=headers)
    s = json.loads(response.text)
    items = s['Items']
    for item in items:
        id = item['Id']
        ChannelTradeNo = item['ChannelTradeNo']
        payid = item['PayPid']
        Tid = item['Tid']
        Time= item['Time']
        timeStr = formatTime(Time)
        TotalFee = item['TotalFee']
        UserId = item['UserId']
        UserName = item['UserName']
        SellerFee = item['SellerFee']
        Yifu = item['Yifu']
        Yingfu = item['Yingfu']
        rate = Rate.query.filter_by(user_id=UserId).first()
        print(UserId)
        if not rate:
            continue
        customRate = rate.rate
        user = User.query.get(UserId)
        baseRate = user.baserate
        tmpRate = customRate - baseRate
        income = TotalFee * tmpRate/100
        # user.balance +=income
        # user.totalIncome += income


        order = Orders(id=id,performance=TotalFee,user_id =UserId,user_name=UserName,ChannelTradeNo=ChannelTradeNo,PayPid=payid,SellerFee=SellerFee,Tid=Tid,Yingfu=Yingfu,Yifu=Yifu,time=timeStr,income=income)
        db.session.add(order)
        db.session.commit()
        #proxy_id,rate,total,orginal_userid,orderid,time

        get_all_ancestors(UserId,customRate,TotalFee,UserId,id,timeStr)


    return make_response(200,'success')

@api_v1.route('/getUsers', methods=['GET','POST'])
def get_testUser():
    url = 'http://yjtx.0534666.com/Manage/UserList?PageNo=1&PageSize=30'
    headers = {'Cookie':'.AspNet.ApplicationCookie=zCT7fSghWi7Z4HyAQuhVIZ0I833ZLbS9pu71QPiQTQDmDKoVzzFugibdMaQ-AaYnbyAOjDMA8EUxlZG1Z1U-IA7GMbIHjtdExwvGWHio7odV1GhxQOekLHUH_muqdvxB21imnRRiNO2lYa7TYo0G5HWIo2-JIRE_xEL8ar-E9SgkySaI0JPlZL7ym1sRVGdRrWDeD28S4iZsN-x66sstO7FeDyDiyEbi73AA5rURUSgWHK2mvHnBpmidv2ncDsCwvPdVTRnewRVGUckVCbjbpwBinH5bt9TnLTNyfabtzqOjWCFBrpgVskjrig9__-593emVSbm3SD2dT2mfIBuEzA'}
    response = requests.get(url=url,headers=headers)
    s = json.loads(response.text)
    items = s['Items']
    for item in items:
        id = item['Id']
        Balance = item['Balance']
        CertNo = item['CertNo']
        Feilv = item['Feilv']
        Fenrun= item['Fenrun']
        Id = item['Id']
        Mobile = item['Mobile']
        Name = item['Name']
        Pid = item['Pid']
        tmpTime = item['Time']
        tre_otherStyleTime = formatTime(tmpTime)

        UserType = item['UserType']
        UserTypeName = item['UserTypeName']
        print(id)
        tmpuser = User.query.get(id)
        if tmpuser:
            # user = User(id=id,name=Name,mobile=Mobile, certno=CertNo, userType=UserType, userTypeName=UserTypeName,baserate=Feilv,pid=Pid,time=tre_otherStyleTime,password='111111')
            # db.session.add(user)
            rate = Rate(user_id=id)
            db.session.add(rate)

        db.session.commit()

    return make_response(200,'success')

def calculate_total_performance(user):
    total_performance = Orders.query.with_entities(db.func.sum(Orders.performance)).filter_by(user_id=user.id).scalar() or 0.0
    for child in user.children:
        total_performance += calculate_total_performance(child)
    return total_performance

def formatTime(timeStr):
    Timestamp = timeStr.replace('/Date(', '').replace(')/', '')
    tre_timeArray = time.localtime(int(Timestamp) / 1000)
    tre_otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", tre_timeArray)
    return tre_otherStyleTime

@api_v1.route('/getperformance', methods=['GET'])
def getperformance():
    data = parseRequest(request)
    user_id = data.get('userid')
    print(user_id)
    top_user = User.query.get(user_id)  # 根据顶级用户的ID获取顶级用户对象
    total_performance = calculate_total_performance(top_user)
    # print(rolist)
    return make_response(200,'success',total_performance)

@api_v1.route('/test', methods=['GET'])
def getp():
    users = User.query.all()
    for user in users:
        user.balance = 0
        user.totalIncome = 0
        print(user.name)
    db.session.commit()

    return make_response(200,'success')



def get_all_ancestors(proxy_id,rate,total,orginal_userid,orderid,time):
    print('get_all_代理')
    def recursive_query(proxy_id,rate,total,orginal_userid,orderid,time):
        proxy = User.query.get(proxy_id)
        print('get_all_代理0',proxy,proxy_id)
        if proxy:
            income = (rate - proxy.baserate)*total/100
            incometype = 0
            type = 0
            if proxy_id == orginal_userid:
                incometype = 0
            else:
                incometype = 1

            proxy.totalIncome += income
            proxy.balance +=income
            incomeData = Income(orderid=orderid,user_id = proxy.id,income=income,incometype=incometype,type=type,time=time)
            print('orderid==',orderid,' userid==',proxy.id,'收入==',income)
            db.session.add(incomeData)
            db.session.commit()

            if proxy.parent_id:
                recursive_query(proxy.parent_id,proxy.baserate,total,orginal_userid,orderid,time)

    recursive_query(proxy_id,rate,total,orginal_userid,orderid,time)