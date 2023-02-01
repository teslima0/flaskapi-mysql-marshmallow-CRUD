from flask import Flask
from flask_jwt_extended import JWTManager


#from flask_jwt_extended.exceptions import JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
db = SQLAlchemy()
def create_app():
    #app= Flask(__name__)
    #db = SQLAlchemy()
    app.config['SECRET_KEY']= '3d74eac695414795926022bc5cdbdd00'
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db" 
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask-api2' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
   
    db.init_app(app)
    jwt = JWTManager(app)
    from .import models

    with app.app_context():
        db.create_all()

    #register view
    from .views import views,deletes
    from .auth import auths

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(deletes, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')

    return app
