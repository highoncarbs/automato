from wtforms import StringField , SelectField , FileField , SelectMultipleField
from wtforms.validators import InputRequired , Optional
from flask_wtf import FlaskForm 
from datetime import datetime

from app import db

class contacts(db.Model):
    __searchable__ = ['business_name' , 'contact_one' , 'contact_two' , 'city']
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
    campaign = db.Column(db.Integer)
    keyword_used = db.Column(db.String(200))

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
    keyword = db.Column(db.String(50))
    meta = db.Column(db.String(500) , default = str(0))

class scrape_form(FlaskForm):  
    city = StringField('city' , validators = [InputRequired() , Optional() ]) 
    keyword = StringField('keyword' , validators = [InputRequired()]) 

class job_form(FlaskForm):  
    city = SelectField('city' , coerce = str) 
    keyword = SelectField('keyword' , coerce = str)
    campaign = SelectField('campaign' , coerce = str)

class template(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100))
    img_path = db.Column(db.String(200) )
    mssg_1 = db.Column(db.String(200) , default = "Hi ,")
    mssg_2 = db.Column(db.String(200) , default = "We are Mfg. of exclusive Hand Block Printed Dress Materials , Dupatta ,Stole ,Sarees , Kurties ,Fabrics , Skirts & much more .")
    mssg_3 = db.Column(db.String(200) , default = "Please visit www.jaitexart.com")
    mssg_4 = db.Column(db.String(200) , default = "Our customers include Fabindia , Westside, Biba, Anita dongre and much more. If you are interested in wholesale purchase (minimum order RS 15,000). Please contact Us.")
    mssg_5 = db.Column(db.String(200) , default = "Thanking You")
    mssg_6 = db.Column(db.String(200) , default = "Hemant Sethia")
    mssg_7 = db.Column(db.String(200) , default = "Jai Texart , Jaipur")
    mssg_8 = db.Column(db.String(200) , default = "+918875666619")

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

class import_file(FlaskForm):
    data_file = FileField('data_file' , validators=[InputRequired()])

class contact_search(FlaskForm):
    search = StringField('search' , validators = [InputRequired()])

class contact_filter(FlaskForm):
    city = SelectMultipleField('city' , coerce =int)
