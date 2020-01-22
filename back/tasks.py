import requests
import time
from app import db ,json
from model import Contact , Scrape , City , Tag , Job, Club ,Template , ClubContactSchema
from huey import SqliteHuey
from sqlalchemy.exc import IntegrityError
import pickle , os

# Selenium Imports

from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Timers
import random

huey = SqliteHuey(filename='./task.db')

place_id_list = []
API_KEY = 'AIzaSyCCNjBph61HIqSnJ5kgLzapqPYyRtEj9DQ'


user_data_wp = os.path.abspath("./user-data-wp")
global chrome_options

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")

chrome_options.add_argument("user-data-dir="+ str(user_data_wp))

global chrome_path
global first_check

chrome_path = r"C:\Users\Padam\Documents\chromedriver\chromedriver.exe"

'''
#Add 
http://api.geonames.org/postalCodeSearchJSON?placename=mumbai&username=padam&maxrows=100
Deep search for City - Get names from 
'''

@huey.task()
def scrape_google(id):
    scraper = Scrape.query.filter_by(id=int(id)).first()
    tags = scraper.tag
    city = scraper.city[0].name
    scraper.status = "running"
    db.session.commit()
    city_obj = City.query.filter_by(id=int(scraper.city[0].id)).first()
    
    meta = json.loads(scraper.meta)
    areas = get_areas(city)

    for item in tags:
        for area in areas:
            print(' It inside areasss')
            search_term = item.name + ' ' + str(area) + ' ' + city

            search_maps(search_term , "")
            tag_obj = Tag.query.filter_by(id=int(item.id)).first()
            
        for r in place_id_list:
            name ,address ,phone , website = get_contact(r)

            try:
                
                new_data = Contact(name, phone, "",address,website , city_obj)
                new_data.tag_contact.append(tag_obj)
                db.session.add(new_data)
                db.session.commit()

            except IntegrityError as e:
                db.session.rollback()
                pass
                
            except Exception as e:
                db.session.rollback()
                print(str(e))
                pass
    
    scraper.status = "done"
    db.session.commit()


def search_maps(search_term, next_page_token):
    search_term = search_term.replace(' ', '+')
    print("Running data extraction for "+search_term)

    SEARCH = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + \
        search_term+"&key="+API_KEY+"&pagetoken="+next_page_token

    data = requests.get(SEARCH).json()

    for place in data['results']:
        if place['place_id'] not in place_id_list:
            place_id_list.append(place['place_id'])

    try:
        next_page_token = data['next_page_token']
        if next_page_token:
            time.sleep(5)
            search_maps(search_term, next_page_token)
        else:
            pass
    except KeyError:
        pass

def get_contact(place_id):
    time.sleep(3)
    DETAIL = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id + \
        "&fields=name,formatted_address,international_phone_number,website&key="+API_KEY
    place_details = requests.get(DETAIL).json()['result']
    try:
        name = place_details['name']
    except KeyError:
        name = ""
    try:
        address = place_details['formatted_address']
    except KeyError:
        address = ""
    try:
        phone_number = place_details['international_phone_number']
        phone_number.replace(" ", "")
    except KeyError:
        phone_number = ''
    try:
        website = place_details['website']
    except KeyError:
        website = ''

    return name, address, phone_number, website



def get_areas(city):
    path = str("http://api.geonames.org/postalCodeSearchJSON?placename={}&username=padam&maxrows=100".format(str(city)))
    data = json.loads(requests.get(path).text)['postalCodes']
    area_in_city = [ x['placeName'] for x in data ]
    return area_in_city

@huey.signal()
def task_signal(signal, task):
    print(task.id)
    print(task)

@huey.task()
def whatsapp(id):
    # Takes in Job ID and sends contacts
    job = Job.query.filter_by(id=int(id)).first()
    template = job.template[0]
    path = job.template[0].path
    message = job.template[0].message

    job.status = "running"
    db.session.commit()
    
    clubs = job.club
    meta = json.loads(job.meta)
    contacts = []
    contact_schema = ClubContactSchema()
    
    #  Needs a meta for cooloff period and which contact to start back from.

    for item in clubs:
        club = Club.query.filter_by(id = int(item.id)).first()
        data = contact_schema.dump(club)['total_contact']
        for inner in data:
            contacts.append(inner)
    
    driver = driver_init()
    if 'last' in meta.keys():
        start_range = int(meta['last'])
    else:
        start_range = int(0)

    end_range = start_range + 100
    
    for contact in contacts[start_range:end_range]:
        try:
            num = contact['contact_one']
            # Replace Message with Name
            num = num.replace('+' ,'')
            num = num.replace('-' ,'')
            num = num.replace(' ', '')
            
            name = contact['name'].split('-')[0]
            if message.find('{name}') is not - 1:
                formated_message = message.replace('{name}', name)
            else:
                formated_message = message
            whatsapp_send(driver , num , meta['timer'] , path , formated_message)
        except Exception as e:
            pass
    job.status = "done"
    meta['last'] = end_range
    job.meta = json.dumps(meta)
    driver.close()
    db.session.commit()

    

def driver_init():
    
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    return driver

def send_mssg(driver , message):
    
    # line_break =  # ActionChain init
    try:
        element = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') # Selecting Input Box
        time.sleep(random.randint(2,4)+round(random.random(),2)) # Wait before sending mssg
        
        message_list = message.split('\n')
        for mssg in message_list:
            element.send_keys(str(mssg))
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            
        time.sleep(random.randint(2,3)+round(random.random(),2)) # Wait before sending mssg
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click() #send mssg
    except Exception as e:
        print(str(e))
        pass

def send_photo(driver , path):
    
    try:
    # Check for Number Not Valid Popup
        attach = WebDriverWait(driver , 20).until(
            EC.element_to_be_clickable((By.XPATH , '//*[@id="main"]/header/div[3]/div/div[2]'))
            )

        attach.click()

        time.sleep(random.randint(2,5)+round(random.random(),2))
        
        img_abs_path = path
        photo = driver.find_element_by_css_selector('#main > header > div._2kYeZ > div > div._3j8Pd.GPmgf > span > div > div > ul > li:nth-child(1) > button > input[type=file]').send_keys(img_abs_path)
        time.sleep(random.randint(3,5)+round(random.random(),2))
        photo_send = driver.find_element_by_css_selector("span[data-icon='send-light']").click()
    except Exception as e:
        print(str(e))
        pass

def first_run_check(*args):
    #  Need global setting of 
    check = 0
    if len(args) is 1:
        check = int(args[0])
    return check
    
def whatsapp_send(driver , num , timer , path , message):
    driver.get('https://web.whatsapp.com/send?phone='+num+'')
    first_check = int(first_run_check())

    if first_check == int(0):
        print("Running First Check")
        time.sleep(random.randint(10, 15) + round(random.random(), 2))
        first_run_check(1) 
    
    # Time sleep for Mobile Device
    time.sleep(int(timer))

    if check_valid_number(driver):
        send_photo(driver , path)
        send_mssg(driver , message)
        time.sleep(random.randint(6,10)+round(random.random(),2)) # setup for Leave page alert
    else:
        
        print("Unable to send to "+num) 

 
def check_valid_number(driver):
    try:
        
        popup = driver.find_element_by_css_selector("#app > div > span:nth-child(2) > div > span > div > div > div > div")
        check_valid = popup.get_attribute("data-animate-modal-popup")
        if check_valid :
            return False 
        else:
            return True
    except Exception as e:
        print("Number seems to be valid : " + str(e) )
        return True

#  Need Reporting Complete Reporting of tools

@huey.task()
def messages(id):
 # Takes in Job ID and sends contacts
    job = Job.query.filter_by(id=int(id)).first()
    template = job.template[0]
    message = job.template[0].message

    job.status = "running"
    db.session.commit()

    clubs = job.club
    meta = json.loads(job.meta)
    contacts = []
    contact_schema = ClubContactSchema()
    driver = driver_init()

    #  Needs a meta for cooloff period and which contact to start back from.
    

    for item in clubs:
        club = Club.query.filter_by(id = int(item.id)).first()
        data = contact_schema.dump(club)['total_contact']
        for inner in data:
            contacts.append(inner)
        

    # Nuber needs 0 before +91 for local indian numbers
    print(contacts)
    print(clubs)
    for contact in contacts:
        print(contact)
        try:
            num = contact['contact_one']
            # Replace Message with Name
            num = num.replace('+' ,'')
            num = num.replace('-' ,'')
            num = num.replace(' ', '')
            num = num[2:12]
            name = contact['name'].split('-')[0]
            if message.find('{name}') is not - 1:
                formated_message = message.replace('{name}', name)
            else:
                formated_message = message
            message_send(driver , num , formated_message)
        except Exception as e:
            print(str(e))
            pass
   
   
    job.status = "done"
    driver.close()
    db.session.commit()

def message_send(driver, num, msg):
    driver.get('https://messages.google.com/web/')
    time.sleep(random.randint(10 , 12) + round(random.random(), 2))

    new_chat = WebDriverWait(driver , 30).until(
            EC.element_to_be_clickable((By.XPATH , '/html/body/mw-app/div/main/mw-main-container/div[1]/mw-main-nav/div/mw-fab-link/a'))
            )
    
    # new_chat = driver.find_element_by_xpath('/html/body/mw-app/div/main/mw-main-container/div[1]/mw-main-nav/div/mw-fab-link/a')
    new_chat.click()

    time.sleep(random.randint(2, 4) + round(random.random(), 2))
    
    # Enter number
    driver.implicitly_wait(10) # seconds

    number_box = WebDriverWait(driver , 30).until(
            EC.element_to_be_clickable((By.XPATH , '//*[@id="mat-chip-list-0"]/div/input'))
            )
    number_box.send_keys(str(num))
    number_box.send_keys(Keys.ENTER)
    
    time.sleep(random.randint(2, 4) + round(random.random(), 2))

    # Message Input Box
    mssg_box = WebDriverWait(driver , 30).until(
            EC.element_to_be_clickable((By.XPATH , '/html/body/mw-app/div/main/mw-main-container/div[1]/mw-conversation-container/div/div/mws-message-compose/div[2]/div/mws-autosize-textarea/textarea'))
            )
    # mssg_box = driver.find_element_by_xpath('/html/body/mw-app/div/main/mw-main-container/div[1]/mw-conversation-container/div/div/mws-message-compose/div[2]/div/mws-autosize-textarea/textarea')
    mssg_box.send_keys(msg)
    
    time.sleep(random.randint(2, 4) + round(random.random(), 2))

    # Click Send Button
    send_button = driver.find_element_by_xpath('/html/body/mw-app/div/main/mw-main-container/div[1]/mw-conversation-container/div/div/mws-message-compose/mws-message-send-button/button')
    send_button.click()

    time.sleep(random.randint(2, 4) + round(random.random(), 2))
