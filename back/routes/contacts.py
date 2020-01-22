import os
from app import app, jsonify, request, json, UPLOAD_FOLDER
from app import db
from app import ma

from sqlalchemy.exc import IntegrityError
import csv


from model import Contact, ContactSchema, ContactBaseSchema, City, Tag


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

    data = chain_data.paginate(page, 20, False).items
    json_data = schema.dump(data)
    return jsonify(json_data)


@app.route('/get/contacts/<id>', methods=['POST'])
def get_contacts_by_id(id):
    schema = ContactSchema()
    data = Contact.query.filter_by(id=int(id)).first()
    json_data = schema.dump(data)
    return jsonify(json_data)


@app.route('/add/contacts', methods=['POST'])
def add_contact():
    payload = request.json
    try:

        city = City.query.filter_by(id=int(payload['city'])).first()
        new_data = Contact(payload['name'], payload['contact_one'],
                           payload['contact_two'], payload['address'], payload['email'], city)

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
        new_data = Contact.query.filter_by(id=int(id)).first()
        new_data.tag_contact = []

        city = City.query.filter_by(id=int(payload['city'])).first()
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
        new_data = Contact.query.filter_by(id=int(id))
        if new_data.first():
            new_data.delete()
            db.session.commit()
            return jsonify({'success': "Data Deleted"})

        else:
            return jsonify({'message': "Data doesn't exists"})
    except Exception as e:
        # return Exception for duplicate data
        print(str(e))


@app.route('/upload/contacts', methods=['POST'])
def upload_contact():
    file = request.files['file']
    tags = json.loads(request.form['data'])
    try:
        if file:
            filename = file.filename
            foldertemp = os.path.join(
                UPLOAD_FOLDER, 'contacts')

            if os.path.exists(foldertemp):
                filetemp = os.path.join(
                    foldertemp, filename)
                file.save(filetemp)
            else:

                os.makedirs(foldertemp)

                filetemp = os.path.join(
                    foldertemp, filename)
                file.save(filetemp)

            with open(filetemp, mode="r") as csv_file:

                csv_data = list(csv.reader(csv_file, delimiter=","))

                for item in csv_data:
                    name = item[0] + '-' + item[1]
                    contact_one = str(item[6])
                    contact_two = str(item[7])
                    address = str(item[2])
                    city = item[3].lower()
                    state = item[4]
                    country = item[5]
                    email = item[8]
                    tag = tags
                    city = city.split('-')[0].split('(')[0]



                    if len(contact_one) == 10:
                        contact_one = '91' + contact_one

                    if city == "":
                        if state == "":
                            city = country
                        else:
                            city = state

                    # Checks for empty values
                    if item[0] is not "":
                    
                        try:
                            city_obj = City.query.filter_by(name=str(city)).first()

                            if city_obj:
                                pass
                            else:
                                
                                city_obj = City(str(city), str(state), str(country))
                                db.session.add(city_obj)

                            con_obj = Contact(name , contact_one , contact_two , address , email , city_obj)
                            db.session.add(con_obj)

                            for item in tag:
                                tag_obj = Tag.query.filter_by(
                                    name=item['name']).first()
                                if tag_obj:
                                    pass
                                else:
                                    pass
                                    tag_obj = Tag(str(item['name']))
                                    db.session.add(tag_obj)

                                con_obj.tag_contact.append(tag_obj)
                            db.session.commit()
                        except IntegrityError as e:
                            db.session.rollback()
                            print('Duplicate ----- '+ name , city  )
                            pass    
                        except Exception as e:
                            db.session.rollback()
                            print('Oh No ---------' , name, city  )
                            pass
                    else:
                        pass
                    
        return jsonify({'success': 'Data Added'})

    except Exception as e:
        # return Exception for duplicate data
        print(str(e))
        return jsonify({'message': 'Returns error'})
