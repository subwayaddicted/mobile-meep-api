import os
import io
from flask import Blueprint, jsonify
from flask_restplus import Api, Resource, reqparse
import meep as mp
from app.meep_api.models.image_transformer import ImageTransformer
from app.meep_api.models.waveguide import Waveguide
import base64
import matplotlib.pyplot as plt

waveguides = Blueprint('waveguides', __name__)
waveguides_api = Api(waveguides, version='0.2.3', title='meep API waveguides', description='waveguides API')
waveguide_namespace = waveguides_api.namespace('waveguides', description='Simple waveguides endpoints')


@waveguide_namespace.route('/cell')
class Cell(Resource):
	@waveguide_namespace.doc('Sets cell')
	@waveguide_namespace.param('x', 'x')
	@waveguide_namespace.param('y', 'y')
	@waveguide_namespace.param('z', 'z')
	@waveguide_namespace.param('preview', 'Whether render preview or not')
	def post(self):
		parser = waveguide_namespace.parser()
		parser.add_argument('preview', type=int, location='args', help='Whether render preview or not')
		parser.add_argument('z', type=int, location='args', help='z')
		parser.add_argument('y', type=int, location='args', help='y')
		parser.add_argument('x', type=int, location='args', help='x')
		args = parser.parse_args()
		waveguide = Waveguide(waveguides, 'straight')

		if args['preview'] == 1:
			waveguide.set_cell(args)
			waveguide.set_geometry()
			waveguide.set_sources()
			waveguide.set_layers()
			waveguide.set_resolution()

			sim = waveguide.simulate(waveguide.data)
			eps_data = sim.get_array(center=mp.Vector3(), size=waveguide.get_cell(), component=mp.Dielectric)
			plt.figure()
			plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
			plt.axis('off')
			fig_electric = plt.gcf()

			waveguide.discard_data()
			waveguide.set_cell(args)

			buffer = io.BytesIO()
			fig_electric.savefig(buffer, format='png')
			buffer.seek(0)
			cell_preview = buffer.read()
			buffer.close()

			return jsonify(
				cell_preview=cell_preview,
				waveguide=waveguide.__dict__
			)

		waveguide.set_cell(args)

		return jsonify(
			waveguide=waveguide.__dict__
		)


@waveguide_namespace.route('/straight-waveguide')
class StraightWaveguide(Resource):
	@waveguide_namespace.doc('Returns test text and computes of e/m wave propagation in straight waveguide')
	@waveguide_namespace.param('waveguide', 'Waveguide')
	def post(self):
		parser = waveguide_namespace.parser()
		parser.add_argument('waveguide', type=object, location='args', help='waveguide object')
		args = parser.parse_args()

		waveguide = args['waveguide']

		waveguide.set_geometry()
		waveguide.set_sources()
		waveguide.set_layers()
		waveguide.set_resolution()

		sim = waveguide.simulate(waveguide.data)
		waveguide.output(sim, 0.7, 50)
		waveguide.image_transform(0.7)

		return jsonify(
			electric='It works and everything is pretty mush ok!'
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
