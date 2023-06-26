from flask_script import Manager
from app import app, db
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

if __name__ == '__main__':
    manager.run()