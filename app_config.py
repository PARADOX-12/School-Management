from flask import Flask,request,jsonify,Blueprint,json
from mongoengine import Document, StringField,Q,EmailField,IntField,DecimalField
from flask_jwt_extended import JWTManager,get_jwt_identity,jwt_required,create_access_token,create_refresh_token
from config import JWT_SECRETE_KEY,JWT_REFRESH_TOKEN,JWT_ACCESS_TOKEN_EXPIRES
from app.utils.database import connect_db
from app.Routes.students import students_route
from app.Routes.class_route import class_route
from app.Routes.Students_assignment import assignment_task
from app.Routes.auth import auth


app = Flask(__name__)
JWTManager(app)
app.config['JWT_SECRET_KEY'] = JWT_SECRETE_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN'] = JWT_REFRESH_TOKEN
connect_db(app)
app.register_blueprint(students_route)
app.register_blueprint(class_route)
app.register_blueprint(assignment_task)
app.register_blueprint(auth)