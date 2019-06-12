
<p align="center">
<img align="center" src="./assets/logo.png">
   <br><br>
<img align="center" src="https://img.shields.io/badge/WORK%20-IN%20PROGRESS-yellow.svg"/>
<img align="center" src="https://img.shields.io/badge/License-MIT-blue.svg"/>
<img align="center" src="https://img.shields.io/badge/Python-3-lightgrey.svg" /> 
<br>
</p>

<p align="center">Web Application to automate sending Whatsapp Messages , SMS &amp; Email campaigns.</p>
<img align="center" src="./assets/herohero.png">

## Features

 * Scrape business data from Justdial , Google Businesses (WIP)
 * Send whatsapp messages automatically to contact groups
 * Manage and edit contact/business (WIP)
 * Import (WIP) / Export Data out of Automato
 * Setup templates for campaigns
 * More to come ...

## Installation (WIP)


*NOTE:* You'll need to use python3. 

To install requirements :

> pip install -r requirements.txt

Automato requires the following softwares to work  , please follow the setup from the offical docs.

* [Selenium](https://www.seleniumhq.org/)
* [RabbitMQ](https://www.rabbitmq.com/#getstarted) as message broker
* [MySQL](https://www.mysql.com/downloads/) as backend database 

Automato needs 3 scripts to work  run.py  ,  scrape.py , whatsapp.py .

> python ./run.py

Runs the flask web application 

>python scrape.py 

Starts the scraper consumer

>python whatsapp.py 

Starts the whatsapp consumer

For a fully end to end connected system , you can contact me for a custom install . Which will include running these scripts from a single source - flask app. Controlling of the scripts straight from the interface. Full windows support.

## Issues and Requests
For any issue or requests , kindly use Github Issues.

## Projects Used
* [Bulma CSS](http://getskeleton.com)
* Flask
* SQLAlchemy
* WTForms
* Albemic

## License
This project is licensed under the [MIT License](./LICENSE).