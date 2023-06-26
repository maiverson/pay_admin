from flask import Blueprint, jsonify, request
from app.models.user import User,Users,Role
from app.models.order import Order
from app import db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import CORS,cross_origin

from config import make_response,parseRequest


api_v1 = Blueprint('api_v1', __name__)
cors = CORS(api_v1)

@api_v1.route('/login', methods=['GET','POST'])
def login():
    data = parseRequest(request)
    username = data.get('username')
    psw = data.get('password')
    print(username,psw)
    user = User.query.filter_by(username=username).first()
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

    user = User.query.filter_by(username=username).first()
    print(user)
    code = 1
    info = '成功'
    json = ''
    if not user:
        code = 0
        info = '请求失败'
    else:
        code = 1
        json = {'name': user.username, 'email': user.email,'avatar':user.avatar,'roles':[user.roles]}

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

    user = User(username=username, email=email,password=psw,avatar=avatar,roles=roles)
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
