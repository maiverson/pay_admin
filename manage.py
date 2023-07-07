from flask_script import Manager
from app import app, db
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

manager = Manager(app)

@manager.command
def create_db():
    print ('创建数据库')
    db.create_all(app=app)

if __name__ == '__main__':
    print ('sss')
    manager.run()