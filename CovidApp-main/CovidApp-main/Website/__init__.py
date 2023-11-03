from flask import Flask
from flask_cors import CORS as cors

def create_app():
    app = Flask(__name__)
    cors(app)
    
    app.config['SECRET_KEY'] = 'secret key'
    from .views import views
    from .API import API

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(API, url_prefix='/')
    return app

