from wtforms import StringField , SelectField
from wtforms.validators import InputRequired , Optional
from flask_wtf import FlaskForm 
from datetime import datetime

from app import db

class contacts(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    business_name = db.Column(db.String(250) , nullable = False )
    contact_one = db.Column(db.String(15))
    contact_two = db.Column(db.String(15))
    address = db.Column(db.String(250))
    website = db.Column(db.String(100))
    tag = db.Column(db.String(500))
    city = db.Column(db.String(50))
    wp_cnt = db.Column(db.Integer , default = 0)
    sms_cnt = db.Column(db.Integer , default = 0)
    email_cnt = db.Column(db.Integer , default = 0)
    provider = db.Column(db.String(50))
    url = db.Column(db.String(300))
    link_hash = db.Column(db.String(150) , unique =True )
    data_hash = db.Column(db.String(150) , unique = True )
    keyword = db.Column(db.String(100))

class scrape_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    keyword = db.Column(db.String(200))
    provider = db.Column(db.String(50))
    status = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True , default=datetime.utcnow)
    meta = db.Column(db.String(500))

class job_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50))
    city = db.Column(db.String(50))
    status = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True , default=datetime.utcnow)
    meta = db.Column(db.String(500))

class scrape_form(FlaskForm):  
    city = StringField('city' , validators = [InputRequired() , Optional() ]) 
    keyword = StringField('keyword' , validators = [InputRequired()]) 

class job_form(FlaskForm):  
    city = SelectField('city' , coerce = str) 