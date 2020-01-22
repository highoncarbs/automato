from app import app , jsonify , request , json
from app import db
from app import ma

from model import Contact, ContactSchema,ContactBaseSchema , City, Tag

@app.route('/get/contacts', methods=['POST'])
def get_contacts():
    payload = request.json
    schema = ContactBaseSchema(many=True)
    sort_order = payload['sort_order']
    sort_by = payload['sort_by']
    page = payload['page']
    
    data = Contact.query
    if sort_by == 'name' and sort_order == "desc":
        chain_data = data.order_by(Contact.name.desc())
    if sort_by == 'name' and sort_order == "asc":
        chain_data = data.order_by(Contact.name.asc())

    # if sort_by == 'city' and sort_order == "desc":
    #     chain_data = data.        .join(model.ClassificationItem).order_by(Contact.city[0].name.desc())

    # if sort_by == 'city' and sort_order == "asc":
    #     chain_data = data.order_by(Contact.city[0].name.asc())
    
    if sort_by == 'id' and sort_order == "asc":
        chain_data = data.order_by(Contact.id.asc())
        
    if sort_by == 'id' and sort_order == "desc":
        chain_data = data.order_by(Contact.id.desc())
    
    if sort_by == 'contact_one' and sort_order == "asc":
        chain_data = data.order_by(Contact.contact_one.asc())

    if sort_by == 'contact_one' and sort_order == "desc":
        chain_data = data.order_by(Contact.contact_one.desc())

    data = chain_data.paginate(page , 20 , False).items 
    json_data = schema.dump(data)
    return jsonify(json_data)

@app.route('/get/contacts/<id>', methods=['POST'])
def get_contacts_by_id(id):
    schema = ContactSchema()
    data = Contact.query.filter_by(id=  int(id)).first() 
    json_data = schema.dump(data)
    return jsonify(json_data)
    
@app.route('/add/contacts', methods=['POST'])
def add_contact():
    payload = request.json
    try:
        city = City.query.filter_by(id = int(payload['city'])).first()
        new_data = Contact(payload['name'], payload['contact_one'], \
         payload['contact_two']  , payload['address'] , payload['email'] ,city)
        
        
        if (len(payload['tags']) is not 0):
                
                for item in payload['tags']:
                    data = Tag.query.filter_by(
                        id=item['id']).first()
                    new_data.tag_contact.append(data)        
        
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'success': "Data added"})

    except Exception as e:
        # return Exception for duplicate data
        print(str(e))
        return jsonify({'message': "Something unexpected happened"})
   
@app.route('/edit/contacts/<id>', methods=['POST'])
def edit_contact(id):
    payload = request.json
    try:
        new_data = Contact.query.filter_by( id = int(id)).first()
        new_data.tag_contact = []
        
        city = City.query.filter_by(id = int(payload['city'])).first()
        new_data.name = payload['name']
        new_data.contact_one = payload['contact_one']
        new_data.contact_two = payload['contact_two']
        new_data.address = payload['address']
        new_data.email = payload['email']

        if (len(payload['tags']) is not 0):
                
                for item in payload['tags']:
                    data = Tag.query.filter_by(
                        id=item['id']).first()
                    new_data.tag_contact.append(data)        
        
        
        db.session.commit()
        return jsonify({'success': "Data added"})

    except Exception as e:
        # return Exception for duplicate data
        print(str(e))
        return jsonify({'message': "Something unexpected happened"})
   

@app.route('/delete/contacts/<id>', methods=['POST'])
def delete_contact(id):
    
    try:
        new_data = Contact.query.filter_by(id = int(id))
        if new_data.first():
            new_data.delete()
            db.session.commit()
            return jsonify({'success': "Data Deleted"})

        else:
            return jsonify({'message': "Data doesn't exists"})
    except Exception as e:
        # return Exception for duplicate data
        print(str(e))   



@app.route('/upload/contacts/<id>', methods=['POST'])
def upload_contact(id):
    payload = request.files
    try:
        new_data = Contact.query.filter_by(id = int(id))
        if new_data.first():
            new_data.delete()
            db.session.commit()
            return jsonify({'success': "Data Deleted"})

        else:
            return jsonify({'message': "Data doesn't exists"})
    except Exception as e:
        # return Exception for duplicate data
        print(str(e))   


