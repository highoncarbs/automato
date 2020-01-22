from app import app , jsonify , request , json , db , ma

from model import Scrape,  ScrapeSchema  ,City , Tag

import tasks

@app.route('/get/scraper', methods=['GET'])
def get_scraper():
    if request.method == 'GET':

        data_schema = ScrapeSchema(many=True)
        data = Scrape.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@app.route('/run/scraper/<id>', methods=['GET'])
def run_scraper(id):
    task = tasks.scrape_google(id)
    return jsonify({'success' : 'Scraper started'})

@app.route('/add/scraper', methods=['POST'])
def add_scraper():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        if payload:
            try:
               if (len(payload['tags']) is not 0):
                city = City.query.filter_by(id = int(payload['city'])).first()
                check_data = Scrape.query.join(City, Scrape.city).filter(Scrape.city.any(City.id == city.id)).first()
                meta = {}
                meta['detail'] = str(payload['detail'])
                if (check_data):
                    tags = check_data.tag
                    check_data.meta = json.dumps(meta)
                    for item in payload['tags']:
                        if item not in tags:
                            data = Tag.query.filter_by(
                                id=item['id']).first()
                            check_data.tag.append(data)    
                else:
                    new_data = Scrape(city)
                    meta = {}
                    meta['detail'] = str(payload['detail'])
                    new_data.meta = json.dumps(meta)
                    for item in payload['tags']:
                        data = Tag.query.filter_by(
                            id=item['id']).first()
                        new_data.tag.append(data)    
                    db.session.add(new_data)
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


@app.route('/edit/scraper', methods=['POST'])
def edit_scraper():
    if request.method == 'POST':
        
        payload = request.json
        if payload['name'] is not None:

            check_data = Scrape.query.filter_by(
                name=payload['name'].lower().strip()).first()
            if check_data and check_data.name != payload['name'].lower().strip():
                return jsonify({'message': 'Data - '+check_data.name+' already exists.'})
            else:
                try:
                    new_data = Scrape.query.filter_by(
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


@app.route('/delete/scraper/<id>', methods=['POST'])
def delete_scraper(id):
    if request.method == 'POST':
        payload = request.json
        check_data = Scrape.query.filter_by(id=int(id))
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
