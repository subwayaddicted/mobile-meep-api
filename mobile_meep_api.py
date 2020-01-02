from flask import Flask
from app.meep_api import api


app = Flask(__name__)
api.init_app(app)
