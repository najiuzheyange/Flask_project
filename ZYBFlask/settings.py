import os

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR=os.path.join(BASE_DIR,"static")
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY='123456'

class RunConfig(Config):
    DEBUG=False