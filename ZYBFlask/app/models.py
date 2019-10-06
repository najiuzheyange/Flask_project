from app import models

class BaseModel(models.Model):
    __abstract__ = True               #申明当前类是抽象类，被继承调用不被创建
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    def save(self):
        db=models.session
        db.add(self)
        db.commit()
    def delete(self):
        db=models.session()
        db.delete(self)
        db.commit()

class User(BaseModel):
    __tablename__="user"
    user_name=models.Column(models.String(32))
    password=models.Column(models.String(32))
    email=models.Column(models.String(32))

class Leave(BaseModel):
    """
    请假人id
    请假人姓名
    假期类型
    假期起始时间
    假期结束时间
    请假描述
    联系方式
    请假状态：请假  批准  驳回   销假
    """
    __tablename__ = "leave"
    request_id = models.Column(models.Integer)
    request_name = models.Column(models.String(32))
    request_type = models.Column(models.String(32))
    request_description = models.Column(models.Text)
    request_start_time = models.Column(models.String(32))
    request_end_time = models.Column(models.String(32))
    request_phone = models.Column(models.String(32))
    request_status = models.Column(models.String(32))