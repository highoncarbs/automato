import csv , os
from app import db 
from model import  Contact , City , Tag
from sqlalchemy.exc import IntegrityError

file_json = r""

path = os.path.abspath(file_json)
with open(path) as f:
    data = csv.reader(f)

tags = ['suit', 'dupatta', 'home', 'skirt', 'pant', 'palazzo', 'tops', 'saree', 'blouse' , 'fabric' , 'dress material' , 'bag' , 'kurti' , 'bedsheet' , 'kurta']
    
def check(string, sub_str): 
    if (string.find(sub_str) != -1):  
        return sub_str


for item in data:

    name = item['contacts_name'] + '-' + item['contacts_company'] 
    contact = str(item['contact_ph_country']) + str(item['contacts_mobile1'])
    city = item['contact_city']
    state = item['contact_state']
    country = item['country_name']
    enquiry = str(item['contact_last_product']).lower()
    tag = [y for y in (check(enquiry, x) for x in tags) if y is not None]
    tag.append('indiamart')

    if city == "":
        if state == "":
            city = country
        else:
            city = state
    
    
    # Checks for empty values
    
    try: 
        city_obj = City.query.filter_by(name=str(city)).first()
        
        if city_obj:
            pass 
        else:
            city_obj = City(str(city), str(state), str(country))
            db.session.add(city_obj)
        

        con_obj = Contact(name , contact , "" , "" , "" , city_obj)
        db.session.add(con_obj)    
        
        for item in tag:
            tag_obj = Tag.query.filter_by(name=item).first()
            if tag_obj:
                pass
            else:
                tag_obj = Tag(str(item))
                db.session.add(tag_obj)
        
            con_obj.tag_contact.append(tag_obj)

        db.session.commit()
        print('Added Data ---- ' + name , city , contact)
    except IntegrityError:
        db.session.rollback()
        print('Duplicate ----- '+ name , city , contact)
        pass    
    except Exception as e:
        db.session.rollback()
        print('Oh No ---------' , name, city , contact )
        pass    


import requests
def check_api():
    data = json.loads(requests.get("http://api.geonames.org/postalCodeSearchJSON?placename=mumbai&username=padam&maxrows=100"))['postalCodes']
    area = [ x['placeName'] for x in data]
    print(area)

if __name__ == "__main__":
    check_api
