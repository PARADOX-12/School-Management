from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

load_dotenv()


def connect_db(app):
    try:
        app.config['MONGODB_SETTINGS'] = {
            'host': os.getenv('uri')
        }

        db = MongoEngine()
        db.init_app(app)

        print('Database connected successfully')


    except Exception as e:
        print("Error occured" , str(e))

