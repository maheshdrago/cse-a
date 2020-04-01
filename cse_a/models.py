
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from cse_a import app
from flask_sqlalchemy import SQLAlchemy
from cse_a import app

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



admin =Admin(app,template_mode='bootstrap3')



admin.add_view(ModelView(Message,db.session))
