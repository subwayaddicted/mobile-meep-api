from flask import Flask
from app.meep_api.controllers.waveguides import waveguides


app = Flask(__name__)
app.register_blueprint(waveguides, url_prefix='/waveguides')
