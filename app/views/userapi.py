from flask import Blueprint, jsonify, request
from app.models.user import User,UserType
from app import db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import CORS,cross_origin
import time
from app.views import make_response,parseRequest
import requests
import json
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import text

user = Blueprint('user', __name__)
cors = CORS(user)

@user.route('/adduser', methods=['GET','POST'])
def addUser():
    data = parseRequest(request)
    print(data)

    username = data.get('name')
    phone = data.get('phone')
    card = data.get('card')
    rate = data.get('rate')
    type = data.get('type')

    userType = UserType.query.get(type)
    status = 1


    print(username,phone,status)
    info = ''
    code = 1
    json = ''
    user = User(name=username, password='111111', userType=userType.id,userTypeName=userType.typename, mobile=phone, certno=card, status=status, baserate=rate)
    db.session.add(user)
    db.session.commit()
    info = '用户添加成功'
    code = 1


    return make_response(code, info, json)


@user.route('/updateuser', methods=['GET','POST'])
def updateUser():
    info = ''
    code = 1
    json = ''

    data = parseRequest(request)
    print(data,request)

    username = data.get('name')
    phone = data.get('phone')
    card = data.get('card')
    rate = data.get('rate')
    type = data.get('type')
    userid = data.get('userid')
    if not userid:
        code = 0
        info = '参数错误'
        return make_response(code, info)

    userType = UserType.query.get(type)
    status = 1

    user = User.query.get(userid)

    user.name = username
    user.userType = userType.id
    user.userTypeName = userType.typename
    user.mobile = phone
    user.certno = card
    user.baserate = rate
    db.session.commit()
    info = '用户编辑成功'
    code = 1


    return make_response(code, info, json)

@user.route('/deleteuser', methods=['GET','POST'])
def deleteUser():
    info = ''
    code = 1
    json = ''

    data = parseRequest(request)
    print(data,request)
    userid = data.get('userid')
    if not userid:
        code = 0
        info = '参数错误'
        return make_response(code, info)

    user = User.query.get(userid)
    if not user:
        code = 0
        info = '用户不存在'
        return make_response(code, info)
    db.session.delete(user)
    db.session.commit()
    info = '用户删除成功'
    code = 1


    return make_response(code, info, json)



@user.route('/getuserist', methods=['GET','POST'])
def getUserList():
    data = parseRequest(request)
    tmppage = data.get('page')
    tmplimit = data.get('limit')
    name = data.get('name')
    type = data.get('type')
    print('类型===',type)
    page = 1
    limit = 20
    # 分页查询
    orderby = data.get('sort')
    if not tmppage:
        page = 1
    else:
        page = int(tmppage)
    if not tmplimit:
        limit = 20
    else:
        limit = int(tmplimit)

    orderStr = text('-time')
    if(orderby):
        orderStr = text(orderby)
    else:
        orderStr = text('-time')

    sql = User.query.order_by(orderStr)
    if name:
        sql = User.query.order_by(orderStr).filter(User.name.contains(name))
    else:
        sql = User.query.order_by(orderStr)

    if type:
        sql = sql.filter_by(userType=type)


    lists = sql.limit(limit).offset((page - 1) * limit).all()
    total_count = sql.count()
    total_pages = (total_count + limit - 1) // limit


    info = ''
    status = 1
    json = ''
    if not lists:
        status = 0
        info = '暂无用户信息'
    else:
        status = 1
        info = '请求成功'

        json = {'items': [item.to_dict() for item in lists ],'total':total_count}


    return make_response(status,info,json)


@user.route('/getusertype', methods=['GET','POST'])
# @jwt_required()
def get_user_info():
    typeList = UserType.query.all()
    code = 1
    info = '成功'
    json = ''
    if not typeList:
        code = 0
        info = '请求失败'
    else:
        code = 1
        json = {'items': [item.to_dict() for item in typeList ]}


    return make_response(code,info,json)

#
# @order.route('/getorderList', methods=['GET','POST'])
# def getAllOrder():
#     orders = Order.query.all()
#
#     info = ''
#     status = 1
#     json = ''
#     if not orders:
#         status = 0
#         info = '暂无订单信息'
#     else:
#         status = 1
#         info = '请求成功'
#         total = Order.query.count()
#         json = {'items': [{'order_no': order.order_no, 'price': order.price,'status':order.status,'timestamp':order.timestamp,'username':order.username} for order in orders],'total':total}
#     return make_response(status,info,json)
#
#
# def get_order_code():
#     #  年月日时分秒+time.time()的后7位
#     order_no ='JD'+ str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
#     return order_no
#
#
# @order.route('/createtablelist', methods=['GET','POST'])
# def createTableList():
#     url = 'http://localhost:9527/dev-api/vue-element-admin/article/list?page=1&limit=100'
#     response = requests.get(url)
#     s = json.loads(response.text)
#
#     items = s['data']['items']
#     for item in items:
#         table = DragTable(id=item['id'], title=item['title'], type=item['type'], author=item['author'], comment_disabled=item['comment_disabled'], content=item['content'],content_short=item['content_short']
#                           ,display_time=item['display_time'],forecast=item['forecast'],image_uri=item['image_uri'],importance=item['importance'],pageviews=item['pageviews'],reviewer=item['reviewer'],status=item['status'],timestamp=item['timestamp'])
#         db.session.add(table)
#     db.session.commit()
#
#     status = 1
#     jsonStr = ''
#
#     info = '请求成功'
#     return make_response(status,info,jsonStr)
#
#
# @order.route('/gettablelist', methods=['GET','POST'])
# def getTableList():
#     data = parseRequest(request)
#     tmppage = data.get('page')
#     tmplimit = data.get('limit')
#     page = 1
#     limit = 20
#     # 分页查询
#
#     if not tmppage:
#         page = 1
#     else:
#         page = int(tmppage)
#     if not tmplimit:
#         limit = 20
#     else:
#         limit = int(tmplimit)
#
#
#     lists = DragTable.query.limit(limit).offset((page - 1) * limit).all()
#     total_count = DragTable.query.count()
#     total_pages = (total_count + limit - 1) // limit
#
#     info = ''
#     status = 1
#     json = ''
#     if not lists:
#         status = 0
#         info = '暂无订单信息'
#     else:
#         status = 1
#         info = '请求成功'
#         json = {'items': [item.to_dict() for item in lists ],'total':total_count}
#
#     return make_response(status,info,json)
#
