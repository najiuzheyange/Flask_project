import hashlib
import functools
import datetime

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


#分页器配置
class Pager():
    """
    分页器需要具备的功能
        页码
        分页数据
        是否第一页
        是否最后一页
    """
    def __init__(self,total_data,page_size):
        """
        :param total_data: 要进行分页的总数据
        :param page_size: 每页多少条数据
        """
        self.total_data=total_data
        self.page_size=page_size
        self.is_start=False
        self.is_end = False
        self.page_count=len(total_data)   #总数据的长度
        self.next_page=0 #下一页
        self.previous_page=0 #上一页
        self.page_number=self.page_count/page_size    #分了多少页
        #判断是否整除，有余数需要在加一页
        if self.page_number == int(self.page_number):
            self.page_number=int(self.page_number)
        else:
            self.page_number=int(self.page_number)+1
        self.page_range=range(1,self.page_number+1)   #最后得到的页码范围
    def page_data(self,page):
        """
        返回的分页数据
        :param page: 页码
        思路：
        page_size=10
        1  start 0  end 10
        2  start 10 end 20
        3  start 20  end 30
        """
        self.next_page=int(page)+1
        self.previous_page=int(page)-1
        if page <=self.page_range[-1]:   #如果页面小等于页码范围最大的数
            page_start = (page -1)*self.page_size
            page_end=page*self.page_size
            data=self.total_data[page_start:page_end]
            if page == 1:
                self.is_start = True
            else:
                self.is_start = False
            if page == self.page_range[-1]:
                self.is_end = True
            else:
                self.is_end = False
        else:
            data=["没有数据"]
        return data

@main.route("/holiday_leave/", methods=["GET", "POST"])
@loginValid
# @csrf.exempt
def holiday_leave():
    if request.method == "POST":
        username = request.form.get("request_name")
        type = request.form.get("request_type")
        start_time = request.form.get("request_start_time")
        end_time = request.form.get("request_end_time")
        phone = request.form.get("request_phone")
        description = request.form.get("request_description")

        leave = Leave()
        leave.request_id = request.cookies.get("id")
        leave.request_name = username
        leave.request_type = type
        leave.request_description = description
        leave.request_start_time = start_time
        leave.request_end_time = end_time
        leave.request_phone = phone
        leave.request_status = "0"
        leave.save()
        return redirect("/leave_list/1/")
    return render_template("holiday_leave.html")


@main.route("/leave_list/<int:page>/")
@loginValid
def leave_list(page):
    leaves = Leave.query.all()
    pager = Pager(leaves, 2)  # 实例化一个分页器leaves为总数据，3为每页的数据条数
    page_data = pager.page_data(page)  # 对应页码所显示的数据
    return render_template("leave_list.html", **locals())

class Calendar():
    def __init__(self,month="now"):
        self.result=[]
        big_month=[1,3,5,7,8,10,12]
        small_month=[4,6,9,11]
        now = datetime.datetime.now()
        #获取指定月份1号日期
        if month == "now":
            month = now.month
            first_date = datetime.datetime(now.year,now.month,1,0,0)
        else:
            first_date=datetime.datetime(now.year,month,1,0,0)
        #获取指定月份的总天数
        if month in big_month:
            day_range=range(1,32)
        elif month in small_month:
            day_range=range(1,31)
        else:
            day_range=range(1,29)
        self.day_range=list(day_range)
        first_week=first_date.weekday()  #获取指定月份1号是周几
        #第一行数据
        line1=[]
        for i in range(first_week):
            line1.append(" ")
        for j in range(7-first_week):
            if j!=4 and j!=5:
                line1.append(str(self.day_range.pop(0))+"-django开发")
            else:
                line1.append(str(self.day_range.pop(0)))
        self.result.append(line1)
        #获取其他日期的数据
        while self.day_range:
            line=[]
            for b in range(7):
                if len(line)<7 and self.day_range and b!=5 and b!=6 :
                    line.append(str(self.day_range.pop(0))+"-django开发")
                elif len(line)<7 and self.day_range:
                    line.append(str(self.day_range.pop(0)))
                else:
                    line.append(" ")
            self.result.append(line)
    def return_month(self):
        return self.result
    def print_month(self):
        print("星期一 星期二 星期三 星期四 星期五 星期六 星期日")
        for line in self.result:
            for e in line:
                e=e.center(6)
                print(e,end=" ")
            print()


@main.route("/userinfo/")
@loginValid
def userinfo():
    calendar=Calendar().return_month()
    now=datetime.datetime.now()
    return render_template("userinfo.html",**locals())