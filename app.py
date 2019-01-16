from flask import Flask , render_template , g , redirect , jsonify , url_for , request , session
from flask_sqlalchemy import SQLAlchemy 
import MySQLdb
import pika 
import json 
import os 
import csv
from werkzeug import secure_filename
from flask_migrate import Migrate 
# from whoosh.analysis import StemmingAnalyzer 
import flask_whooshalchemy 
import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
from model import contacts , scrape_form , scrape_task , job_form , job_task , template , template_form
migrate = Migrate(app , db)

global visit
visit = 0

def connect_queue():
    if not hasattr(g , 'rabbitmq'):
        g.rabbitmq = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return g.rabbitmq

def get_scraper_queue():
    if not hasattr(g ,'task_queue'):
        conn = connect_queue()
        channel = conn.channel()
        channel.queue_declare(queue = 'scraper_queue' , durable=True)
        channel.queue_bind(exchange='amq.direct' , queue = 'scraper_queue')
        g.task_queue = channel 
    return g.task_queue 

def destroy_scraper_queue():
    if hasattr(g , 'task_queue'):
        g.task_queue.queue_delete(queue = "scraper_queue")
    else:
        print("Scraper Queue not availabel")

def get_mssg_queue():
    if not hasattr(g ,'mssg_queue'):
        conn = connect_queue()
        channel = conn.channel()
        channel.queue_declare(queue = 'mssg_queue' , durable=True)
        channel.queue_bind(exchange='amq.direct' , queue = 'mssg_queue')
        g.mssg_queue = channel 
    return g.mssg_queue 


@app.teardown_appcontext
def close_queue(error):
    if hasattr(g , 'rabbitmq'):
        g.rabbitmq.close()


@app.route('/' , methods = ['GET' , 'POST'])
def home():

    global visit 
    if visit is 0:
        visit = 1
        session['mssg'] = " 👋   Hello there !"
    else:
        session['mssg'] = ""
    con_len = db.session.query(contacts).count()
    city_len = db.session.query(contacts.city).distinct(contacts.city).count()

    src_len = db.session.query(scrape_task).count()
    src_fin = db.session.query(scrape_task).filter_by(status = str(2)).count()
    src_unfin = db.session.query(scrape_task).filter_by(status = str(0)).count()
    src_run = db.session.query(scrape_task).filter_by(status = str(1)).count()

    job_len = db.session.query(job_task).count()
    job_fin = db.session.query(job_task).filter_by(status = str(2)).count()
    job_unfin = db.session.query(job_task).filter_by(status = str(3)).count()
    print(job_unfin)
    job_run = db.session.query(job_task).filter_by(status = str(1)).count()

    return render_template('dash.html' , con_len = con_len , city_len = city_len , src_len = src_len , src_fin = src_fin ,\
        src_unfin = src_unfin , src_run = src_run , job_len = job_len , job_fin = job_fin ,\
        job_unfin = job_unfin , job_run = job_run , mssg = session['mssg']) , 200

@app.route('/scheduler' ,methods = ['GET' , 'POST'])
def scheduler():
    return render_template('scheduler.html') , 200



@app.route('/jobs' ,methods = ['GET' , 'POST'])
def jobs():
    form = job_form()
    def_city = ('0' , 'Select City')

    form.city.choices = [def_city] + [ (r.city , r.city ) for r in db.session.query(scrape_task) ]

    form.keyword.choices = [(r.keyword , r.keyword) for r in db.session.query(scrape_task.keyword).distinct(scrape_task.keyword)]
    form.campaign.choices = [(r.name , r.name) for r in db.session.query(template)]

    job_list = db.session.query(job_task).all()
    if form.validate_on_submit():
        city = form.city.data 
        keyword = form.keyword.data 
        provider = "Whatsapp"
        # Check if the city and keyword already exsists ?
        check_one = db.session.query(job_task).filter_by(city = city , provider = provider , keyword = keyword).first()
        if check_one is None:
            new_job = job_task(city = city  , provider = provider , status = str(0) , meta = str('') , keyword = keyword)
            db.session.add(new_job)
            db.session.commit()
            session['mssg'] = " 👍 Job added to list."
            return redirect('/jobs')
        else:
            session['mssg'] = " 🙃 Job already exsists. You can re-run the job from the list below , or run a new job with different parameters."
            return redirect('/jobs')
    else:
        print(form.errors)
    return render_template('jobs.html' , form= form , job_list = job_list , mssg = session['mssg']) , 200

@app.route('/contacts' ,methods = ['GET' , 'POST'])
def contacts_call():
    # contacts_list = db.session.query(contacts).all()
    return render_template('contacts.html' ) , 200

@app.route('/task_pause' , methods = ['POST'])
def task_pause(task_id):
    # Destroys the queue and the message 
    pass

@app.route('/scraper', methods = ['GET' , 'POST'])
def scraper():
    form = scrape_form()
    scraper_list = db.session.query(scrape_task).all()
    print(scraper_list)
    if form.validate_on_submit():
        city = str(form.city.data).title() 
        keyword = form.keyword.data  
        provider = "Justdial"
        # Check if the city and keyword already exsists ?
        check_one = db.session.query(scrape_task).filter_by(city = city , keyword = keyword , provider = provider).first()
        if check_one is None:
            new_scraper =scrape_task(city = city , keyword = keyword , provider = provider , status = str(0) , meta = str(1))
            db.session.add(new_scraper)
            db.session.commit()
            session['mssg'] = " 👍 Scraper added to list."
            
            return redirect('/scraper')
        else:
            session['mssg'] = " 🙃 Job already exsists. You can re-run the job from the list below , or run a new job with different parameters."
            return redirect('/scraper')
    return render_template('scraper.html' , form= form  ,scraper_list = scraper_list , mssg = session['mssg']) , 200


@app.route('/push_scraper_to_queue/<task_id>' , methods = ['POST' , 'GET'])
def push_scraper_to_queue(task_id):

    # Pushes the task to scraper run queue 
    # Runs only one task a time 
    try:
        task = db.session.query(scrape_task).filter_by(id = task_id).first()
        search_data = {'city' : task.city , 'keyword' : task.keyword , 'page' : task.meta , 'task_id' : task_id}
        q = get_scraper_queue()
        q.basic_publish(
            exchange='amq.direct',
            routing_key='scraper_queue',
            body=json.dumps(search_data),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        task.status = 1
        db.session.commit()
        session['mssg'] = " 👷 Will start scraping {} for {} soon .".format()

        return redirect('/scraper')
    except Exception as e:
        mssg = "We ran into an error : " + str(e)
        print(mssg)
        return redirect('/scraper')

@app.route('/push_job_to_queue/<task_id>' , methods = ['POST' , 'GET'])
def push_job_to_queue(task_id):

    # Pushes the task to scraper run queue 
    # Runs only one task a time 
    try:
        task = db.session.query(job_task).filter_by(id = task_id).first()
        job_data = {'city' : task.city ,'meta' : task.meta , 'task_id' : task_id , 'keyword' : task.keywordS}
        m = get_mssg_queue()
        m.basic_publish(
            exchange='amq.direct',
            routing_key='mssg_queue',
            body=json.dumps(job_data),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        task.status = 1
        db.session.commit()
        return redirect('/jobs')
    except Exception as e:
        mssg = "We ran into an error : " + str(e)
        print(mssg)
        return redirect('/jobs')

@app.route('/job_results/<job_id>' , methods= ['POST' , 'GET'])
def job_results(job_id):
    try:
        job_city = db.session.query(job_task).filter_by(id = str(job_id)).first().city
        success_all = db.session.query(contacts).filter_by(city = job_city).filter((contacts.wp_cnt == 1)).all()
        invalid_all = db.session.query(contacts).filter_by(city = job_city).filter((contacts.wp_cnt == -2)).all()
        jdnum_all = db.session.query(contacts).filter_by(city = job_city).filter((contacts.wp_cnt == 0)).all()
        unable_all = db.session.query(contacts).filter_by(city = job_city).filter((contacts.wp_cnt == -1)).all()

        # success_sent = [x if x.wp_cnt is 1 else None for x in contacts]
        # invalid_sent = [x if x.wp_cnt is -2 else None for x in contacts]
        # jd_number = [x if x.wp_cnt is 0 else None for x in contacts]
        # unable_Sent = [x if x.wp_cnt is -1 else None for x in contacts]
        
        return jsonify({'success_all' : len(success_all) , 'invalid_all' : len(invalid_all)})
    except Exception as e:
        pass
        return "Naah" + str(e)

@app.route('/src_results/<job_id>/<keyword>' , methods= ['POST' , 'GET'])
def src_results(job_id , keyword):
    try:
        src_city = db.session.query(scrape_task).filter_by(id = str(job_id)).first().city
        success_all = db.session.query(contacts).filter_by(city = src_city).filter_by(keyword = keyword).all()
        # success_sent = [x if x.wp_cnt is 1 else None for x in contacts]
        # invalid_sent = [x if x.wp_cnt is -2 else None for x in contacts]
        # jd_number = [x if x.wp_cnt is 0 else None for x in contacts]
        # unable_Sent = [x if x.wp_cnt is -1 else None for x in contacts]
        
        return jsonify({'con_all' : len(success_all)})
    except Exception as e:
        pass
        return "Naah" + str(e)
@app.route('/task_report/<job_id>' , methods = ['POST' , 'GET'])
def task_report(job_id):
    # Endpoint for full report for JOB and TASK Results
    # TO-DO for next release
    pass


UPLOAD_FOLDER = os.path.abspath('./static/images/uploads/')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/templates' , methods = ['POST' , 'GET'])
def templates():

    temps = db.session.query(template).all()
    form = template_form()
    if form.validate_on_submit():
        if request.method == 'POST':
            file = request.files['img']
            try:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    img_temp = os.path.join(UPLOAD_FOLDER, filename) 
                    file.save(img_temp)
                    name = form.name.data
                    mssg_1 = form.mssg_1.data 
                    mssg_2 = form.mssg_2.data 
                    mssg_3 = form.mssg_3.data 
                    mssg_4 = form.mssg_4.data 
                    mssg_5 = form.mssg_5.data 
                    mssg_6 = form.mssg_6.data 
                    mssg_7 = form.mssg_7.data 
                    mssg_8 = form.mssg_8.data 
                    if mssg_1 or mssg_2 or mssg_3 or mssg_4 or mssg_5 or mssg_6 or mssg_7 or mssg_8 is '' :
                        new_temp = template(name = name ,img_path = filename )
                    else:
                        new_temp = template(name = name , mssg_1 = mssg_1 , img_path = filename , mssg_2 = mssg_2 , mssg_3 = mssg_3 ,\
                            mssg_4 = mssg_4, mssg_5 = mssg_5, mssg_6 = mssg_6, mssg_7 = mssg_7 , mssg_8 = mssg_8)
                    db.session.add(new_temp)
                    db.session.commit()
                    mssg = "Template successfully added"
                    print(mssg)
                    return redirect(url_for('templates'))
            except Exception as e:
                print(str(e))
    return render_template('templates.html' , form = form ,temps = temps) , 200

@app.route('/del_temp/<id>' , methods=['POST' , 'GET'])
def del_temp(id):
    try:
        temp = db.session.query(template).filter_by(id = id)
        temp.delete()
        db.session.commit()
        mssg = "Template Deleted Successfully"
        return redirect(url_for('templates'))
    except Exception as e:
        print(str(e))
        return redirect(url_for('templates')) , 200


@app.route('/jobcombo/<city>' , methods = ['POST' , 'GET'])
def jobcombo(city):
    job_city = city
    keyword = [r.keyword for r in db.session.query(scrape_task.keyword).distinct(scrape_task.keyword).filter((scrape_task.city == str(city))).all()]
    print(keyword)
    return jsonify({'options' : keyword})

@app.route('/message/session' , methods=['POST'])
def mssg_del():
    session['mssg'] = ""
    return jsonify({'mssg' :'Emptying session mssg' })

@app.route('/export/all' , methods=['POST'])
def export_all():

    backup_folder = os.path.abspath('./backups')
    con_all = db.session.query(contacts)
    jobs = db.session.query(job_task)
    scrape = db.session.query(scrape_task)

    folder_date = datetime.datetime.now()
    folder_name = str(folder_date.strftime("%c"))
    folder_name = folder_name.replace(" " , "_").replace(":" , "-")

    try:
        backup_fol = backup_folder + '\\' + folder_name
        os.makedirs(backup_fol)
        backup_con = backup_fol +  '\\contacts.csv'
        backup_job = backup_fol +  '\\jobs.csv'
        backup_scrape = backup_fol +  '\\scrape.csv'

        with open(backup_con, 'w') as contacts_file:
            outcsv = csv.writer(contacts_file, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

            header = contacts.__table__.columns.keys()

            outcsv.writerow(header)     

            for record in con_all.all():
                outcsv.writerow([getattr(record, c) for c in header ])
        
        with open(backup_job , 'w') as job_file:
            outcsv_j = csv.writer(job_file, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

            header = job_task.__table__.columns.keys()

            outcsv_j.writerow(header)     

            for record in jobs.all():
                outcsv_j.writerow([getattr(record, c) for c in header ])
        
        with open(backup_scrape, 'w') as job_file:
            outcsv = csv.writer(job_file, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

            header = scrape_task.__table__.columns.keys()

            outcsv.writerow(header)     

            for record in scrape.all():
                outcsv.writerow([getattr(record, c) for c in header ])
        
            
        #     return "Success"
        # except Exception as e:
        #     print(str(e))
        # return ""
    except Exception as e:
        print(str(e))
    return "UH"