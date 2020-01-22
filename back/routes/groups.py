from app import app , jsonify , request , json , db , ma

from model import Club, ClubSchema , Contact , Tag , City


@app.route('/get/club', methods=['GET'])
def get_club():
    if request.method == 'GET':

        data_schema = ClubSchema(many=True)
        data = Club.query.all()
        print(data)
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@app.route('/add/club', methods=['POST'])
def add_club():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        if len(payload['name']) != 0:

            check_data = Club.query.filter_by(name=payload['name'].lower().strip())
            if check_data.first():
                return jsonify({'message': 'Data - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Club(
                        payload['name'].lower().strip())
                    if (len(payload['contacts']) != 0):
                        for item in payload['contacts']:
                            print(item)
                            data = Contact.query.filter_by(id=int(item['id'])).first()
                            new_data.contact.append(data)

                        db.session.add(new_data)
                        db.session.commit()
                        return jsonify({'success': 'Data Added'})
                    
                    else:
                        tag = payload['tags']
                        city = payload['city']
                        for item in tag:
                            print(item)
                            data = Tag.query.filter_by(id=int(item['id'])).first()
                            new_data.tag.append(data)
                        
                        for item in city:
                            data = City.query.filter_by(id=int(item['id'])).first()
                            new_data.city.append(data)

                    
                        db.session.commit()
                    return jsonify({'success': 'Data Added'})

                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@app.route('/edit/club', methods=['POST'])
def edit_club():
    if request.method == 'POST':
        
        payload = request.json
        if payload['name'] is not None:

            check_data = Club.query.filter_by(
                name=payload['name'].lower().strip()).first()
            if check_data and check_data.name != payload['name'].lower().strip():
                return jsonify({'message': 'Data - '+check_data.name+' already exists.'})
            else:
                try:
                    new_data = Club.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name'].lower().strip()
                    new_data.state = payload['state'].lower().strip()
                    new_data.country = payload['country'].lower().strip()
                    db.session.commit()
                    return jsonify({'success': 'Data Updated'})

                except Exception as e:
                    print(str(e))

                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@app.route('/delete/club/<id>', methods=['POST'])
def delete_club(id):
    if request.method == 'POST':
        payload = request.json
        check_data = Club.query.filter_by(id=int(id))
        if check_data.first():
            try:
                check_data.delete()
                db.session.commit()
                return jsonify({'success': 'Data deleted'})
            except Exception as e:
                db.session.rollback()
                db.session.close()
                return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})
