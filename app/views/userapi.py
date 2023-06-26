from flask import Blueprint, jsonify, request
from app.models.user import ClientUser
from app import db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import CORS,cross_origin
import time
from app.views import make_response,parseRequest
import requests
import json
from sqlalchemy_serializer import SerializerMixin

user = Blueprint('user', __name__)
cors = CORS(user)

@user.route('/adduser', methods=['GET','POST'])
def addUser():
    data = parseRequest(request)
    username = data.get('username')
    password = data.get('password')
    avatar = data.get('avatar')
    phone = data.get('phone')
    status = 1


    print(username,password,avatar,phone,status)
    info = ''
    code = 1
    json = ''
    order = ClientUser(userName=username, password=password, avatar=avatar, phone=phone, status=status)
    db.session.add(order)
    db.session.commit()
    info = '用户添加成功'
    code = 1


    return make_response(code, info, json)


@user.route('/getuserist', methods=['GET','POST'])
def getUserList():
    data = parseRequest(request)
    tmppage = data.get('page')
    tmplimit = data.get('limit')
    page = 1
    limit = 20
    # 分页查询

    if not tmppage:
        page = 1
    else:
        page = int(tmppage)
    if not tmplimit:
        limit = 20
    else:
        limit = int(tmplimit)


    lists = ClientUser.query.limit(limit).offset((page - 1) * limit).all()
    total_count = ClientUser.query.count()
    total_pages = (total_count + limit - 1) // limit

    info = ''
    status = 1
    json = ''
    if not lists:
        status = 0
        info = '暂无订单信息'
    else:
        status = 1
        info = '请求成功'
        json = {'items': [item.to_dict() for item in lists ],'total':total_count}

    return make_response(status,info,json)


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
