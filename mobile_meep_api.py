from flask import Flask, jsonify
from flask_restplus import Api, Resource
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import h5py

app = Flask(__name__)
api = Api(app, version='0.1', title='meep API', description='meep package used as API')

ns_waveguides = api.namespace('waveguides', description='Simple waveguides endpoints')


@ns_waveguides.route('/straight-waveguide')
class StraightWaveguide(Resource):
	@api.doc('Returns b64 encoded image of e/m wave propagation in straight waveguide')
	def get(self):
		cell = mp.Vector3(16, 8, 0)

		geometry = [
			mp.Block(
				mp.Vector3(mp.inf, 1, mp.inf),
				center=mp.Vector3(),
				material=mp.Medium(epsilon=12))
		]

		sources = [mp.Source(
			mp.ContinuousSource(frequency=0.15),
			component=mp.Ez,
			center=mp.Vector3(-7, 0))
		]

		pml_layers = [mp.PML(1.0)]

		resolution = 10

		sim = mp.Simulation(
			cell_size=cell,
			boundary_layers=pml_layers,
			geometry=geometry,
			sources=sources,
			resolution=resolution)

		sim.use_output_directory()

		sim.run(mp.at_every(0.6, mp.output_png(mp.Ez, "-Zc /home/NIX/novitsky/PycharmProjects/mobile-meep-api/colormaps/dkbluered")), until=200)

		return jsonify(
			electric='test message atm 5'
		)
