# -*- coding: utf-8 -*-

# Whatsapp Bot for sending Mass messages 
# Worker RabbitMQ

from selenium import webdriver 
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import socket
import pika 
import threading
import functools
import json
from app import db 
from model import contacts , job_task
import os
import logging 

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")

logging.basicConfig(
    filename='automato_whatsapp.log',
    level=logging.DEBUG,
    format='[automato-whatsapp] %(levelname)-7.7s %(message)s'
)

global chrome_path
global task_id_g
global num_g
global first_run_check
global payload
global timer
first_run_check = 0

RABBITMQ_HOST = 'localhost'
credentials = pika.PlainCredentials('guest' , 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost' , credentials = credentials))
channel = connection.channel()
channel.queue_declare(queue='mssg_queue' , durable= True)
channel.basic_qos(prefetch_count = 1)
threads = []

def driver_init():
    global driver 
    driver = webdriver.Chrome(chrome_path , chrome_options= chrome_options)

def send_mssg():
    
    actions = ActionChains(driver) # ActionChain init
    element = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') # Selecting Input Box
    time.sleep(1) # Wait before sending mssg
    element.send_keys(payload["mssg_1"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()
    element.send_keys(payload["mssg_2"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()
    element.send_keys(payload["mssg_3"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()
    element.send_keys(payload["mssg_4"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()

    element.send_keys(payload["mssg_5"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()

    element.send_keys(payload["mssg_6"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()

    element.send_keys(payload["mssg_7"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()

    element.send_keys(payload["mssg_8"])
    actions.key_down(Keys.SHIFT)
    actions.key_down(Keys.ENTER)
    actions.key_up(Keys.ENTER)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    actions.reset_actions()

    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click() #send mssg
   
def send_photo():
    
    # Check for Number Not Valid Popup
    attach = WebDriverWait(driver , 20).until(
        EC.element_to_be_clickable((By.XPATH , '//*[@id="main"]/header/div[3]/div/div[2]'))
        )

    attach.click()

    time.sleep(1)
    # Absolute Path for Image in Template
    img_abs_path = os.path.abspath('./static/images/uploads/' +str(payload['img_path'] ))
    photo = driver.find_element_by_css_selector('#main > header > div._2kYeZ > div > div._3j8Pd.GPmgf > span > div > div > ul > li:nth-child(1) > button > input[type=file]').send_keys(img_abs_path)
    time.sleep(3)
    photo_send = driver.find_element_by_css_selector("span[data-icon='send-light']").click()
 
def is_connected():
    # Checks for INternet Connectivity
    try:
        socket.create_connection(("www.google.com" , 80))
        return True 
    except:
        is_connected()


def check_valid_number():
    try:
        
        popup = driver.find_element_by_css_selector("#app > div > span:nth-child(2) > div > span > div > div > div > div")
        check_valid = popup.get_attribute("data-animate-modal-popup")
        if check_valid :
            return False 
        else:
            return True
    except Exception as e:
        logging.info("Number seems to be valid : " + str(e) )
        return True

def ack_message(channel , delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass

def consume_stop():
    channel.basic_cancel()

def on_message(channel , method_frame ,header_frame , body , args):
    (connection , threads) = args 
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target= send_messages, args = (connection , channel , delivery_tag , body))
    t.start()
    threads.append(t)

def whatsapp_send(num):
    driver.get('https://web.whatsapp.com/send?phone='+num+'')
    wp_sent = db.session.query(contacts).filter( (contacts.contact_one == str(num)) | (contacts.contact_two == str(num) )).first()
    global first_run_check
    if first_run_check is 0:
        time.sleep(10)
        first_run_check = 1 
    time.sleep(int(timer))
    if check_valid_number():
        send_photo()
        send_mssg()
        wp_sent.wp_cnt = 1
        db.session.commit()
        time.sleep(6) # setup for Leave page alert
    else:
        wp_sent.wp_cnt = -2
        db.session.commit()
        logging.info("Not Valid : Unable to send to "+num) 

def send_messages(connection , channel , delivery_tag , body):
    
    thread_id = threading.get_ident() 
    fmt = 'Thread id: {} Delivery Tag: {} Message body: {}'
    mssg_data = json.loads(body.decode('utf-8'))
    
    city = mssg_data['city']
    task_id = mssg_data['task_id']
    
    global task_id_g
    task_id_g = task_id
    
    meta = mssg_data['meta'] 
    
    global payload
    payload = mssg_data['payload']
    
    global timer 
    timer = mssg_data['timer']
    
    global chrome_path
    chrome_path = mssg_data['user_path']
    # Template loaded from JSON payload via RabbitMQ
    driver_init()

    
    job = db.session.query(job_task).filter_by(id= task_id).first()
    con_all = db.session.query(contacts).filter_by(city = city).filter((contacts.wp_cnt == 0) | (contacts.wp_cnt == -1)).all()
    t_num = [x.contact_one for x in con_all]
    o_num = [x.contact_two for x in con_all]
    numbers = list(set(t_num+o_num))
    numbers.remove('')
   
    if not numbers:
        try: 
            cb = functools.partial(ack_message , channel , delivery_tag)
            connection.add_callback_threadsafe(cb)        
            job.status = 2 # Resume
            db.session.commit()
            driver.close()
            logging.info("Task Done")
        except Exception as e:
            logging.error("Uh oh!  - " + str(e))
    else:

        for num in numbers[:100]:
            check_sent = db.session.query(contacts).filter( (contacts.contact_one == str(num)) | (contacts.contact_two == str(num) )).first()
            global num_g
            num_g = num
            # if check_sent.wp_cnt != str(1) or str(-2) :     
            if is_connected():
                wp_sent = db.session.query(contacts).filter( (contacts.contact_one == str(num)) | (contacts.contact_two == str(num) )).first()
                try:        
                    whatsapp_send(num)
                except Exception as e:
                    try:
                        wp_sent.wp_cnt = -1 
                        db.session.commit()
                        logging.info("Unable to send to "+num)
                        
                    except Exception as e:
                        logging.error("Unable to send to " + num + " - Uh Oh! - " + str(e))

            else:
                job.meta = str(num)
                db.session.commit()
                logging.info("Internet doesn't seem to be running! Closing down send jobs!")
                 

        try: 
            cb = functools.partial(ack_message , channel , delivery_tag)
            connection.add_callback_threadsafe(cb)        
            job.status = 3 # Resume
            db.session.commit()
            driver.close()
            logging.info("Task Done")
        except Exception as e:
            logging.error("Uh Oh! - " + str(e))
   


threads = []
on_message_callback = functools.partial(on_message , args=(connection , threads))
channel.basic_consume(on_message_callback , queue='mssg_queue')

try:
    with open("../wp_run_dat.txt" , "w") as f:
        f.write('1')
    logging.info("Whatsapp Consumer Started")
    channel.start_consuming()

except KeyboardInterrupt:
    with open("wp_run_dat.txt" , "w") as fw:
        fw.write('0')
    cb = functools.partial(ack_message , channel , delivery_tag)
    connection.add_callback_threadsafe(cb)
    channel.queue_purge(queue='mssg_queue')
    channel.queue_delete(queue='mssg_queue')
    channel.close()
    connection.close()

for thread in threads:
    thread.join()
