from flask import Flask, jsonify
from flask_restplus import Api, Resource
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
api = Api(app, version='0.1', title='meep API', description='meep package used as API')


@api.route('/straight-waveguide')
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

		sim.run(until=200)

		eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)

		ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
		plt.figure()
		plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
		plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
		plt.axis('off')
		fig_electric = plt.gcf()

		buffer = BytesIO()
		fig_electric.savefig(buffer, format='png')
		buffer.seek(0)
		electric_b64 = base64.b64encode(buffer.read()).decode()
		buffer.close()

		return jsonify(
			electric=electric_b64
		)
