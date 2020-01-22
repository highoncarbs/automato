from app import db
from app import ma
from datetime import datetime

from marshmallow_sqlalchemy import field_for
from marshmallow import fields




# Contact Template
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    contact_one = db.Column(db.String(50) , unique=True , default= None, nullable = False)
    contact_two = db.Column(db.String(50) , default="")
    address = db.Column(db.String(500) ,  default="")
    email = db.Column(db.String(200) ,  default="")
    city = db.relationship(
        'City', cascade="all,delete", secondary='city_contact', backref='city_contact', lazy='joined')

    def __init__(self, name, contact_one, contact_two, address, email, city):
        self.name  = name
        self.contact_one  = contact_one
        self.contact_two  = contact_two
        self.address  = address
        self.email  = email
        self.city.append(city)


 
db.Table('city_contact',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('city_id', db.Integer, db.ForeignKey(
             'city.id', ondelete='SET NULL')),
         db.Column('contact_id', db.Integer, db.ForeignKey(
             'contact.id', ondelete='SET NULL'))
         )
         



class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) )
    state = db.Column(db.String(100) , default = "")
    country = db.Column(db.String(100) ,  default = "")

    def __init__(self, name, state, country):
        self.name = name
        self.state = state
        self.country = country
   
class CitySchema(ma.ModelSchema):
    id = field_for(City, 'id', dump_only=True)
    name = field_for(City, 'name', dump_only=True)
    state = field_for(City, 'state', dump_only=True)
    country = field_for(City, 'country', dump_only=True)
    
    class meta:
        model = City


db.Table('tag_contact',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('tag_id', db.Integer, db.ForeignKey(
             'tag.id', ondelete='SET NULL')),
         db.Column('contact_id', db.Integer, db.ForeignKey(
             'contact.id', ondelete='SET NULL'))
         )

         
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.relationship(
        'Contact', cascade="all,delete", secondary='tag_contact', backref='tag_contact', lazy='joined')
    def __init__(self, name):
        self.name = name

class TagSchema(ma.ModelSchema):
    id = field_for(Tag, 'id', dump_only=True)
    name = field_for(Tag, 'name', dump_only=True)
    
    class meta:
        model = Tag

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) , unique = True)
    path = db.Column(db.String(200) , default = "")
    message = db.Column(db.String(500) , default= "")
    filetype = db.Column(db.String(100))

    def __init__(self, name, message, filetype):
        self.name  = name
        self.message = message
        self.filetype = filetype
        
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.relationship(
        'Contact', cascade="all,delete", secondary='club_contact', backref='club_contact', lazy='joined')
    tag = db.relationship(
        'Tag', cascade="all,delete", secondary='club_tag', backref='club_tag', lazy='joined')
    city = db.relationship(
        'City', cascade="all,delete", secondary='club_city', backref='club_city', lazy='joined')
    
    def __init__(self, name):
        self.name = name
    
    def get_contacts(self):
        return len(self.contact)

db.Table('club_contact',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('club_id', db.Integer, db.ForeignKey(
             'club.id', ondelete='SET NULL')),
         db.Column('contact_id', db.Integer, db.ForeignKey(
             'contact.id', ondelete='SET NULL'))
         )
db.Table('club_tag',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('club_id', db.Integer, db.ForeignKey(
             'club.id', ondelete='SET NULL')),
         db.Column('tag_id', db.Integer, db.ForeignKey(
             'tag.id', ondelete='SET NULL'))
         )
db.Table('club_city',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('club_id', db.Integer, db.ForeignKey(
             'club.id', ondelete='SET NULL')),
         db.Column('city_id', db.Integer, db.ForeignKey(
             'city.id', ondelete='SET NULL'))
         )

class TemplateSchema(ma.ModelSchema):
    id = field_for(Template, 'id', dump_only=True)
    name = field_for(Template, 'name', dump_only=True)
    path = field_for(Template, 'path', dump_only=True)
    message = field_for(Template, 'message', dump_only=True)
    filetype = field_for(Template, 'filetype', dump_only=True)

    class meta:
        model = Template

class Scrape(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.relationship(
        'City', cascade="all,delete", secondary='city_scrape', backref='city_scrape', lazy='joined')
    status = db.Column(db.String(10) , default="start")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tag = db.relationship(
        'Tag', cascade="all,delete", secondary='tag_scrape', backref='tag_scrape', lazy='joined')
    meta= db.Column(db.String(250) , default="")
    def __init__(self, city):
        self.city.append(city)


db.Table('tag_scrape',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('tag_id', db.Integer, db.ForeignKey(
             'tag.id', ondelete='SET NULL')),
         db.Column('scrape_id', db.Integer, db.ForeignKey(
             'scrape.id', ondelete='SET NULL'))
         )
db.Table('city_scrape',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('city_id', db.Integer, db.ForeignKey(
             'city.id', ondelete='SET NULL')),
         db.Column('scrape_id', db.Integer, db.ForeignKey(
             'scrape.id', ondelete='SET NULL'))
         )

class ScrapeSchema(ma.ModelSchema):
    id = field_for(Scrape, 'id', dump_only=True)
    status = field_for(Scrape, 'status', dump_only=True)
    timestamp = field_for(Scrape, 'timestamp', dump_only=True)
    city = ma.Nested(CitySchema , many = True)
    tag = ma.Nested(TagSchema, many=True)
    

class ContactSchema(ma.ModelSchema):
    id = field_for(Contact, 'id', dump_only=True)
    name = field_for(Contact, 'name', dump_only=True)
    contact_one = field_for(Contact, 'contact_one', dump_only=True)
    contact_two = field_for(Contact, 'contact_two', dump_only=True)
    address = field_for(Contact, 'address', dump_only=True)
    email = field_for(Contact, 'email', dump_only=True)
    city = ma.Nested(CitySchema , many = True)
    tag_contact = ma.Nested(TagSchema , many = True)
    class meta:
        model = Contact

class ContactBaseSchema(ma.ModelSchema):
    id = field_for(Contact, 'id', dump_only=True)
    name = field_for(Contact, 'name', dump_only=True)
    contact_one = field_for(Contact, 'contact_one', dump_only=True)
    contact_two = field_for(Contact, 'contact_two', dump_only=True)
    address = field_for(Contact, 'address', dump_only=True)
    email = field_for(Contact, 'email', dump_only=True)
    city = ma.Nested(CitySchema , many = True)
    class meta:
        model = Contact


db.Table('club_job',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('club_id', db.Integer, db.ForeignKey(
             'club.id', ondelete='SET NULL')),
         db.Column('job_id', db.Integer, db.ForeignKey(
             'job.id', ondelete='SET NULL'))
         )
db.Table('template_job',
         db.Column('id', db.Integer, primary_key=True),
         db.Column('template_id', db.Integer, db.ForeignKey(
             'template.id', ondelete='SET NULL')),
         db.Column('job_id', db.Integer, db.ForeignKey(
             'job.id', ondelete='SET NULL'))
         )


class ClubSchema(ma.ModelSchema):
    id = field_for(Club, 'id', dump_only=True)
    name = field_for(Club, 'name', dump_only=True)
    tag = ma.Nested(TagSchema , many= True)
    city = ma.Nested(CitySchema , many= True)
    total = fields.Method('get_contacts_len')
     
    def get_contacts_len(self, obj):
        # base_city = Contact.query.join(City, Contact.city)
        # base_tag = Contact.query.join(Tag, Contact.tag_contact)

        # base = base_city.union(base_tag)
        if (len(obj.tag) == 0 and len(obj.city) != 0):
            total = len([t for x in obj.city for t in x.city_contact])
           
        elif (len(obj.city) == 0 and len(obj.tag) != 0):
            total = len([c for x in obj.tag for c in x.contact])

        elif (len(obj.city) != 0 and len(obj.tag) != 0):

            total_city = [t for x in obj.city for t in x.city_contact]
            total_tag = [c for x in obj.tag for c in x.contact]
            total = len( set(total_city) & set(total_tag))
        else:
            total = 0
        return { 'contact' : len(obj.contact) , 'tag': total }

    class meta:
        model = Club

class ClubContactSchema(ma.ModelSchema):
    id = field_for(Club, 'id', dump_only=True)
    total_contact = fields.Method('get_contacts')
     
    def get_contacts(self, obj):
        # base_city = Contact.query.join(City, Contact.city)
        # base_tag = Contact.query.join(Tag, Contact.tag_contact)

        # base = base_city.union(base_tag)
        if (len(obj.tag) == 0 and len(obj.city) != 0):
            total = [t for x in obj.city for t in x.city_contact]
           
        elif (len(obj.city) == 0 and len(obj.tag) != 0):
            total = [c for x in obj.tag for c in x.contact]

        elif (len(obj.city) != 0 and len(obj.tag) != 0):

            total_city = [t for x in obj.city for t in x.city_contact]
            total_tag = [c for x in obj.tag for c in x.contact]
            total = set(total_city) & set(total_tag)
        else:
            total = 0
        
        schema = ContactBaseSchema(many=True)
        
        return schema.dump(total)
    
    
    class meta:
        model = Club


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.relationship(
        'Club', cascade="all,delete", secondary='club_job', backref='club_job', lazy='joined')
    status = db.Column(db.String(10) , default="start")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    template = db.relationship(
        'Template', cascade="all,delete", secondary='template_job', backref='template_job', lazy='joined')
    meta = db.Column( db.String(250) , default = None)
    

class JobSchema(ma.ModelSchema):
    id = field_for(Scrape, 'id', dump_only=True)
    status = field_for(Job, 'status', dump_only=True)
    timestamp = field_for(Job, 'timestamp', dump_only=True)
    meta = field_for(Job, 'meta', dump_only=True)
    club = ma.Nested(ClubSchema , many = True)
    template = ma.Nested(TemplateSchema, many=True)
