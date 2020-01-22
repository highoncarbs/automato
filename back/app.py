import logging
import os
from flask import Flask, request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from werkzeug.debug import DebuggedApplication
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
from sqlalchemy.exc import IntegrityError 
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

UPLOAD_FOLDER = os.path.abspath(app.config['UPLOAD_FOLDER'])


db = SQLAlchemy(app)
migrate = Migrate(app ,db)
ma = Marshmallow(app)

from routes import templates , contacts , city , tag , scraper , groups , job , settings
