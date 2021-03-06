from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_wtf.csrf import CSRFProtect   #导入csrf保护
from flask_restful import Api
from flask_migrate import Migrate
pymysql.install_as_MySQLdb()

#实例化插件
csrf=CSRFProtect()
models=SQLAlchemy()
api=Api()

def create():
    """
    生成app配置
    """
    app=Flask(__name__)  #创建app
    app.config.from_object("settings.Config")
    models.init_app(app)  #相当于models=SQLALchemy(app)
    # csrf.init_app(app)
    api.init_app(app)   #加载restful插件
    #导入蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 返回app
    return app
