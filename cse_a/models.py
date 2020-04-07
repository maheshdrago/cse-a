
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from cse_a import app
from flask_sqlalchemy import SQLAlchemy
from cse_a import app
import datetime
db = SQLAlchemy(app)

ENV = 'dev'

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:mahesh6273766@localhost/CSE-A'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']=''



class Message(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    message = db.Column(db.Text())

    def __init__(self,name,email,message):
        self.name = name
        self.email = email
        self.message = message


class Attendance(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,default=datetime.datetime.now())
    present = db.Column(db.Text())


    def __init__(self,present):

        self.present = present

class Cse_Gallery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60))

class Technical(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(40))
    description = db.Column(db.Text())


admin =Admin(app,template_mode='bootstrap3')



admin.add_view(ModelView(Message,db.session))
admin.add_view(ModelView(Attendance,db.session))
admin.add_view(ModelView(Cse_Gallery,db.session))
admin.add_view(ModelView(Technical,db.session))
