from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        from .Models import User, BlogPost
        db.create_all()
    from .views import views
    from .API import API


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(API, url_prefix='/')
    return app


