from flask import Blueprint

main=Blueprint("main",__name__)

from . import views    #执行一遍views文件里的视图