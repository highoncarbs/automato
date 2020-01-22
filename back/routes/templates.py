from app import app , jsonify , request , json , UPLOAD_FOLDER , IntegrityError
from app import db
from app import ma
import os , shutil 

from model import Template  , TemplateSchema

@app.route('/get/template', methods=['GET'])
def get_template():
    schema = TemplateSchema(many=True)
    data = Template.query.all()
    return jsonify(schema.dump(data))
    
@app.route('/add/template', methods=['POST'])
def add_template():
    payload = request.json
    payload = json.loads(request.form['data'])
    file = request.files
    if payload :
        try:
            new_data = Template(
                    payload['name'], payload['message'] ,payload['filetype'] )

            if len(file) != 0:
                    file = request.files['image']
                    try:

                        if file :
                            filename =file.filename
                            foldertemp = os.path.join(
                                UPLOAD_FOLDER, 'templates')

                            if os.path.exists(foldertemp):
                                filetemp = os.path.join(
                                    foldertemp, filename)
                                file.save(filetemp)
                                setattr(new_data, 'path', filetemp)
                            else:

                                os.makedirs(foldertemp)

                                filetemp = os.path.join(
                                    foldertemp, filename)
                                file.save(filetemp)
                                setattr(new_data, 'path', filetemp)
                        else:
                            return jsonify({'message': 'Image file not supported.'})

                    except IntegrityError as e:
                        print(str(e))
                        return jsonify({'message': 'Image file not supported.'})


                    except Exception as e:
                        print(str(e))

            db.session.add(new_data)
            db.session.commit()
            return jsonify({'success': "Data added"})

        except Exception as e:
            # return Exception for duplicate data
            print(str(e))
            return jsonify({'message': "Something went wrong"})
 

@app.route('/delete/template/<id>', methods=['POST'])
def delete_template(id):
    
    try:
        new_data = Template.query.filter_by(id = int(id))
        if new_data.first():
            if len(new_data.first().template_job) is 0:

                new_data.delete()
                db.session.commit()
                return jsonify({'success': "Data Deleted"})
            else:
                return jsonify({'message': "Cannot delete - in use by a job"})

        else:
            return jsonify({'message': "Data doesn't exists"})
    except Exception as e:
        # return Exception for duplicate data
        print(str(e))    
