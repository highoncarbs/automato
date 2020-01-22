from app import app , jsonify , request , json , db , ma

from model import City, CitySchema

@app.route('/get/city', methods=['GET'])
def get_city():
    if request.method == 'GET':

        data_schema = CitySchema(many=True)
        data = City.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@app.route('/add/city', methods=['POST'])
def add_city():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        if len(payload['name']) != 0:

            check_data = City.query.filter_by(name=payload['name'].lower().strip())
            if check_data.first():
                return jsonify({'message': 'Data - '+check_data.first().name+' already exists.'})
            else:
                try:
                    if 'state' not in payload.keys():
                        payload['state'] = ""
                    if 'country' not in payload.keys():
                        payload['country'] = ""

                    new_data = City(
                        payload['name'].lower().strip() , payload['state'].lower().strip() , payload['country'].lower().strip())

                    db.session.add(new_data)
                    db.session.commit()
                    json_data = { 'id' : new_data.id , 'name' : new_data.name}
                    return jsonify({'success': 'Data Added', 'data' : json_data})

                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@app.route('/edit/city', methods=['POST'])
def edit_city():
    if request.method == 'POST':
        
        payload = request.json
        if payload['name'] is not None:

            check_data = City.query.filter_by(
                name=payload['name'].lower().strip()).first()
            if check_data and check_data.name != payload['name'].lower().strip():
                return jsonify({'message': 'Data - '+check_data.name+' already exists.'})
            else:
                try:
                    new_data = City.query.filter_by(
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


@app.route('/delete/city', methods=['POST'])
def delete_city():
    if request.method == 'POST':
        payload = request.json
        check_data = City.query.filter_by(id=payload['id'])
        if check_data.first():
            if len(check_data.first().city_contact) is int(0):
                try:
                    check_data.delete()
                    db.session.commit()
                    return jsonify({'success': 'Data deleted'})
                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
            else:
                return jsonify({'message': 'Cannot delete data. Being used by other master.'})

        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})
