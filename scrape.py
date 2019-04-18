# Scraper Worker - RabbitMQ 

# TODO SOmethign is not right , after adding the project contacts append scenes

from selenium import webdriver 
import time 
import MySQLdb
from app import db
import hashlib 
from selenium.webdriver.chrome.options import Options  
import pika 
import json
import model
import threading
import functools
from model import contacts , scrape_task , Project
from app import curr_project , json 

RABBITMQ_HOST = 'localhost'
_DELIVERY_MODE_PERSISTENT=2

chrome_options = Options()  
chrome_options.add_argument("--disable-popup-blocking")   # Doesn't seem to work!


global chrome_path
global task_id_g
global last_page_g

# Store current user in Scrape task , fetch the user driver path from there
# Update the chrome_path with that.


credentials = pika.PlainCredentials('guest' , 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost' , credentials = credentials))

channel = connection.channel()
channel.queue_declare(queue='scraper_queue', durable=True)
channel.basic_qos(prefetch_count=1)
threads = []

def driver_init():
    global driver 
    driver = webdriver.Chrome(chrome_path , chrome_options= chrome_options)

def scrape_page(city , search_term , page_no):
    driver.get("https://www.justdial.com/" + str(city) + "/" + str(search_term) + "/page-" + str(page_no))
    
    current_url = driver.current_url
    print(current_url)

    if 'rloop' not in str(current_url) and str(city) in str(current_url):
        
        SCROLL_PAUSE_TIME = 1.5
        url_check = True


        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            popup = driver.find_elements_by_xpath('//*[@id="best_deal_div"]/section/span')
            if( popup is True ):
                popup.click()
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(SCROLL_PAUSE_TIME)


        lists = driver.find_elements_by_class_name("cntanr")
        final_list = []
        for lis in lists:
            final_list.append(str(lis.get_attribute("data-href")))
    
        return final_list , url_check
    
    else:
        final_list = []
        url_check = False
        return final_list , url_check

def get_data(list_url):
    driver.get(list_url)

    # Business Name    
    name = driver.find_elements_by_xpath('//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/h1/span/span')
    name = name[0].text #result
    
    #Phone Details
    # contact_numbers = driver.find_elements_by_class_name('#comp-contact > span.telnowpr > a')
    # print(len(contact_numbers))
    mobile = driver.find_elements_by_css_selector('#comp-contact > span.telnowpr > a.tel.mtel')
    mobile_2 = driver.find_elements_by_css_selector('#comp-contact > span.telnowpr > a.tel.ttel')

    phone_keys = {'9d011' : '+' , '9d010' : '9' , '9d001' : '0' , '9d002' : '1' , '9d006' : '5' , '9d007' : '6' , '9d008': '7', '9d009' : '8' , '9d003' : '2' , '9d004' : 3 ,'9d005' : '4' }

    try :
        if len(mobile) is not 0  :
            phone_no = []
            for index in range(1 , 14):
                x = driver.execute_script("return window.getComputedStyle(document.querySelector('#comp-contact > span.telnowpr > a.tel.mtel > span:nth-child("+str(index)+")'),'::before').getPropertyValue('content')")
                # print(phone_keys[ str(repr(x))[7:12]])
                phone_no.append(phone_keys[ str(repr(x))[7:12] ])
                phone_final = ''.join(map(str ,phone_no))
        else:
            phone_final = ""
    except:
        phone_final = ""

    try :

        if len(mobile_2) is not 0:
            phone_no_2 = []
            for index in range(1 , 14):
                x_2 = driver.execute_script("return window.getComputedStyle(document.querySelector('#comp-contact > span.telnowpr > a.tel.ttel > span:nth-child("+str(index)+")'),'::before').getPropertyValue('content')")
                # print(phone_keys[ str(repr(x))[7:12]])
                phone_no_2.append(phone_keys[ str(repr(x_2))[7:12] ])
                phone_final_2 = ''.join(map(str ,phone_no_2))
        else:
            phone_final_2 = ""            
    except:
        phone_final_2 = ""

    #Address
    address = driver.find_elements_by_xpath('//*[@id="fulladdress"]/span/span')
    address = address[0].text #result

    #Tags
    try:

        tags = driver.find_elements_by_xpath('//*[@id="setbackfix"]/div[1]/div/div[4]/div[1]/div[4]/ul')
        tag = str(tags[0].text).replace('\n' , ' ') # result
    except:
        tag = None
    #website
    website = driver.find_elements_by_xpath('//*[@id="comp-contact"]/li[3]/span/a')
    
    if website :
        website = website[0].text # result
    else :
        website = ""

    return name ,phone_final, phone_final_2 ,address , website , tag


def data_is_extracted(connection, channel , delivery_tag , body):
    # Run scrape with city and key word with pages 5 pages
    #  at a time , save last page scraped 
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery Tag: {} Message body: {}'
    search_data = json.loads(body)
    city = search_data['city']
    keyword = search_data['keyword']
    meta = search_data['page']
    task_id = search_data['task_id']
    global task_id_g
    task_id_g = task_id
    global chrome_path
    chrome_path = search_data['user_path']
    print("--------------------------------"+chrome_path)
    driver_init()

    last_page = 0
    project_active  = Project.query.filter_by(id = int(search_data['project'])).first()
    task = db.session.query(scrape_task).filter_by(id = task_id).first()

    for page in range( int(meta) ,100):
        
        result_links , url_check  = scrape_page(city , keyword , str(page))
        global last_page_g
        last_page_g = page
        last_page = page

    
        
        try:
            if url_check and len(result_links) is not 0 : # While Url_check returns True

                for res in result_links:

                    enc_link = hashlib.md5(str(res).encode('utf-8')).hexdigest() # Encodes the link
                    check_one = db.session.query(contacts).filter_by(link_hash = enc_link) # Checks if encoded URL already exsists
                    name , phone_no , phone_no_2 , address , website , tag = get_data(str(res)) 
                    name = str(name)
                    enc_data = hashlib.md5(str(phone_no).encode('utf-8') + str(phone_no_2).encode('utf-8')).hexdigest() # Encodes data into md5 hash
                    new_data = model.contacts(business_name = name , contact_one = phone_no ,
                                contact_two = phone_no_2  , address = address , website = website,
                                tag = tag, link_hash = enc_link , data_hash = enc_data , url = str(res) , provider = "Justdial" , city = city , keyword = keyword)
                    try:
                        if check_one.first():
                            if check_one.filter_by(data_hash = enc_data).filter_by(link_hash = enc_link).first() is None :    
                                db.session.add(new_data)
                                project_active.contact.append(new_data)

                                db.session.commit()
                                print('okay done')
                            else:
                                print('not done , already there')
                                pass

                        else:
                            print('okay very new')

                            db.session.add(new_data)
                            project_active.contact.append(new_data)

                            db.session.commit()
                    
                    except Exception as e:
                        print('couldnt do shit' + str(e))
                        db.session.rollback()
            else:
                break
        except :        
            task.meta = last_page
            db.session.commit()
    
    
    try: 
        cb = functools.partial(ack_message , channel , delivery_tag)
        connection.add_callback_threadsafe(cb)        
        task = db.session.query(scrape_task).filter_by(id = int(task_id)).first()
        task.status = 2
        task.meta = last_page
        db.session.commit()
        driver.close()
        print("Task Done")
    except Exception as e:
        print("Somethign Happeded - " + str(e))

def ack_message(channel , delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass
    
def stop_curr_proc():
    current_url = driver.current_url
    
def consume_stop():
    channel.basic_cancel()

def on_message(channel , method_frame ,header_frame , body , args):
    (connection , threads) = args 
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target= data_is_extracted , args = (connection , channel , delivery_tag , body))
    t.start()
    threads.append(t)


threads = []
on_message_callback = functools.partial(on_message , args=(connection , threads))
channel.basic_consume(on_message_callback , queue='scraper_queue')

try:
    channel.start_consuming()
except Exception as e:
    cb = functools.partial(ack_message , channel , delivery_tag)
    connection.add_callback_threadsafe(cb)
    task = db.session.query(scrape_task).filter_by(id = int(task_id_g)).first()
    task.status = 1
    task.meta = last_page_g
    db.session.commit()
    driver.close()


for thread in threads:
    thread.join()


