from app import app , jsonify , request , json , db , ma

from model import Job, JobSchema , Club , Template , ClubContactSchema

import tasks
@app.route('/get/job', methods=['GET'])
def get_job():
    if request.method == 'GET':

        data_schema = JobSchema(many=True)
        data = Job.query.all()
        json_data = data_schema.dump(data)

        return jsonify(json_data)



@app.route('/run/job', methods=['POST'])
def run_job():
    payload = request.json
    print(payload)
    job = Job.query.filter_by(id=int(payload['curr_id'])).first()
    meta = json.loads(job.meta)
    meta['timer'] =  payload['timer']
    job.meta = json.dumps(meta)
    db.session.commit()
    try:
        task = tasks.whatsapp(job.id)
        print("heheheheheheheeh" + task.args)
        job.status = "running"
        db.session.commit()
        return jsonify({'success': 'Job started'})
    except Exception as e:
        return jsonify({'message': 'Unable to run job. Check logs'})
        
    
@app.route('/run/job/sms', methods=['POST'])
def run_job_sms():
    payload = request.json
    job = Job.query.filter_by(id=int(payload['curr_id'])).first()
    try:
        task = tasks.messages(job.id)
        return jsonify({'success': 'Job started'})
    except Exception as e:
        return jsonify({'message': 'Unable to run job. Check logs'})
        
    
@app.route('/add/job', methods=['POST'])
def add_job():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        if payload:
            try:
               if (len(payload['club']) is not 0):
                template = Template.query.filter_by(id = int(payload['template'])).first()
                new_data = Job()
                new_data.template.append(template)
                meta = {'type': payload['type']}
                new_data.meta = json.dumps(meta)
                for item in payload['club']:
                    print(item)
                    data = Club.query.filter_by(
                        id=item['id']).first()
                    new_data.club.append(data)    
                    
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


@app.route('/edit/job', methods=['POST'])
def edit_job():
    if request.method == 'POST':
        
        payload = request.json
        if payload['name'] is not None:

            check_data = Job.query.filter_by(
                name=payload['name'].lower().strip()).first()
            if check_data and check_data.name != payload['name'].lower().strip():
                return jsonify({'message': 'Data - '+check_data.name+' already exists.'})
            else:
                try:
                    new_data = Job.query.filter_by(
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



@app.route('/delete/job/<id>', methods=['POST'])
def delete_job(id):
    
    try:
        new_data = Job.query.filter_by(id = int(id))
        if new_data.first():
            new_data.delete()
            db.session.commit()
            return jsonify({'success': "Data Deleted"})

        else:
            return jsonify({'message': "Data doesn't exists"})
    except Exception as e:
        # return Exception for duplicate data
        print(str(e))   