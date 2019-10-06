import hashlib
import functools

from flask import request
from flask import redirect
from flask import session
from flask import render_template
from . import main
from app.models import *



def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result



def loginValid(fun):
    @functools.wraps(fun)
    def inner(*args,**kwargs):
        cookie_username=request.cookies.get("username")
        cookie_id=request.cookies.get("id","0")
        user=User.query.get(int(cookie_id))
        session_username=session.get("username")
        if user:
            if user.user_name==cookie_username and session_username==cookie_username:
                return fun(*args,**kwargs)
            else:
                return redirect("/login/")
        else:
            return redirect("/login/")
    return inner

@main.route("/logout/")
def logout():
    response=redirect("/login/")
    response.delete_cookie("username")
    response.delete_cookie("email")
    response.delete_cookie("id")
    del session["username"]
    return response

@main.route("/base/")
def base():
    return render_template('base.html',**locals())

@main.route("/index/")
@loginValid
def index():
    return render_template('index.html',**locals())

@main.route("/login/",methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email).first()
        if user:
            db_password=user.password
            password=setPassword(password)
            if password==db_password:
                response=redirect("/index/")
                response.set_cookie("username",user.user_name)
                response.set_cookie("email",user.email)
                response.set_cookie("id",str(user.id))
                session["username"]=user.user_name
                return response
            else:
                error="密码错误"
        else:
            error="用户不存在"
    return render_template("login.html",error=error)

@main.route("/register/",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        user=User()
        user.user_name=username
        user.password=setPassword(password)
        user.email=email
        user.save()

    return render_template("register.html",**locals())
