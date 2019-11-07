import os
from flask import Blueprint, jsonify
from flask_restplus import Api, Resource
import meep as mp
from app.models.image_transformer import ImageTransformer
import base64

waveguides = Blueprint('waveguides', __name__)
waveguides_api = Api(waveguides, version='0.2.2', title='meep API', description='meep package used as API')
waveguide_namespace = waveguides_api.namespace('waveguides', description='Simple waveguides endpoints')


@waveguide_namespace.route('/straight-waveguide')
class StraightWaveguide(Resource):
	@waveguide_namespace.doc('Returns test text and computes of e/m wave propagation in straight waveguide')
	def get(self):
		root_dir = os.path.dirname(waveguides.root_path)
		dir_out = 'mobile-meep-out/straight'
		colormap = os.path.join(root_dir, 'static', 'colormaps', 'dkbluered')

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

		sim.use_output_directory(dir_out)

		sim.run(mp.at_every(0.6, mp.output_png(mp.Ez, "-Zc" + colormap)), until=200)

		image_transformer = ImageTransformer(dir_out)
		image_transformer.png_to_gif()

		return jsonify(
			electric='test message atm 51'
		)


@waveguide_namespace.route('/ninety-degree-bend')
class NinetyDegreeBend(Resource):
	@waveguide_namespace.doc('Returns test text and computes of e/m wave propagation in 90 degree bend waveguide')
	def get(self):
		root_dir = os.path.dirname(waveguides.root_path)
		dir_out = 'mobile-meep-out/ninety-degree-bend'
		colormap = os.path.join(root_dir, 'static', 'colormaps', 'dkbluered')

		cell = mp.Vector3(16, 16, 0)
		geometry = [mp.Block(
			mp.Vector3(12, 1, mp.inf),
			center=mp.Vector3(-2.5, -3.5),
			material=mp.Medium(epsilon=12)),
			mp.Block(
				mp.Vector3(1, 12, mp.inf),
				center=mp.Vector3(3.5, 2),
				material=mp.Medium(epsilon=12))]
		pml_layers = [mp.PML(1.0)]
		resolution = 10

		sources = [mp.Source(
			mp.ContinuousSource(wavelength=2 * (11 ** 0.5), width=20),
			component=mp.Ez,
			center=mp.Vector3(-7, -3.5),
			size=mp.Vector3(0, 1))]

		sim = mp.Simulation(
			cell_size=cell,
			boundary_layers=pml_layers,
			geometry=geometry,
			sources=sources,
			resolution=resolution)

		sim.use_output_directory(dir_out)

		sim.run(mp.at_every(0.6, mp.output_png(mp.Ez, "-Zc" + colormap)), until=200)

		image_transformer = ImageTransformer(dir_out)
		image_transformer.png_to_gif()

		gif_path = dir_out + '-' + 'movie.gif'
		gif = open(gif_path, 'rb')
		gif_encoded = base64.b64encode(gif.read()).decode()

		return jsonify(
			electric='gif_encoded'
		)