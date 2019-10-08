from flask import Blueprint
from flask_restful import Api

main=Blueprint("main",__name__)
api = Api(main)
from . import views    #执行一遍views文件里的视图