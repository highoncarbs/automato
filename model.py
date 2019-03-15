from wtforms import StringField , SelectField , FileField , SelectMultipleField
from wtforms.validators import InputRequired , Optional
from flask_wtf import FlaskForm 
from datetime import datetime

from app import db


# Flask Forms

class LoginForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')

class SignupForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')
    email = StringField('email')

class scrape_form(FlaskForm):  
    city = StringField('city' , validators = [InputRequired() , Optional() ]) 
    keyword = StringField('keyword' , validators = [InputRequired()]) 

class job_form(FlaskForm):  
    city = SelectField('city' , coerce = str) 
    keyword = SelectField('keyword' , coerce = str)
    campaign = SelectField('campaign' , coerce = str)

class template_form(FlaskForm):
    name = StringField('name' , validators=[InputRequired()])
    img = FileField('img')
    mssg_1 = StringField('mssg_1')
    mssg_2 = StringField('mssg_2')
    mssg_3 = StringField('mssg_3')
    mssg_4 = StringField('mssg_4')
    mssg_5 = StringField('mssg_5')
    mssg_6 = StringField('mssg_6')
    mssg_7 = StringField('mssg_7')
    mssg_8 = StringField('mssg_8')

# DB models 

class template(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100))
    img_path = db.Column(db.String(200) )
    job_id = db.Column(db.Integer, db.ForeignKey('job_task.id'))
    mssg_1 = db.Column(db.String(200) , default = "Hi ,")
    mssg_2 = db.Column(db.String(200) , default = "We are Mfg. of exclusive Hand Block Printed Dress Materials , Dupatta ,Stole ,Sarees , Kurties ,Fabrics , Skirts & much more .")
    mssg_3 = db.Column(db.String(200) , default = "Please visit www.jaitexart.com")
    mssg_4 = db.Column(db.String(200) , default = "Our customers include Fabindia , Westside, Biba, Anita dongre and much more. If you are interested in wholesale purchase (minimum order RS 15,000). Please contact Us.")
    mssg_5 = db.Column(db.String(200) , default = "Thanking You")
    mssg_6 = db.Column(db.String(200) , default = "Hemant Sethia")
    mssg_7 = db.Column(db.String(200) , default = "Jai Texart , Jaipur")
    mssg_8 = db.Column(db.String(200) , default = "+918875666619")

class Users(db.Model):
    id = db.Column(db.Integer ,  primary_key = True) 
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(250))
    # relation to projects

class Project(db.Model):
    pass 
    # Table to hold projects

class scrape_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    keyword = db.Column(db.String(200))
    provider = db.Column(db.String(50))
    status = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True , default=datetime.utcnow)
    meta = db.Column(db.String(500))
    # Project id it belongs to one to many

class job_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50))
    city = db.Column(db.String(50))
    status = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True , default=datetime.utcnow)
    keyword = db.Column(db.String(50))
    meta = db.Column(db.String(500) , default = str(0))
    template =  db.relationship('template', backref='job_task', lazy=True) #One to one mapping
    # Project id it belongs to one to many
