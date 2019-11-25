import os
from flask import Blueprint, jsonify
from flask_restplus import Api, Resource, reqparse
import meep as mp
from app.meep_api.models.image_transformer import ImageTransformer
from app.meep_api.models.waveguide import Waveguide
from app.meep_api.models.cellmodel import CellModel
from app.meep_api.models.geometrymodel import GeometryModel

waveguides = Blueprint('waveguides', __name__)
waveguides_api = Api(waveguides, version='0.3.0', title='meep API waveguides', description='waveguides API')
waveguide_namespace = waveguides_api.namespace('waveguides', description='Simple waveguides endpoints')


@waveguide_namespace.route('/cell')
class Cell(Resource):
	@waveguide_namespace.doc('Sets cell')
	@waveguide_namespace.param('x', 'x coordinate of the field')
	@waveguide_namespace.param('y', 'y coordinate of the field')
	@waveguide_namespace.param('z', 'z coordinate of the field')
	@waveguide_namespace.param('waveguide_type', 'Waveguide type (list of available)')
	def post(self):
		cell = CellModel()
		cell_parser = cell.parse_request(waveguide_namespace)
		args = cell_parser.parse_args()

		waveguide_args = {
			'data':{
				'cell': {}
			},
			'waveguide_type':str
		}

		for arg in args:
			if arg == 'waveguide_type':
				waveguide_args['waveguide_type'] = args[arg]
				break
			waveguide_args['data']['cell'][arg] = args[arg]

		return jsonify(
			waveguide_args=waveguide_args
		)


@waveguide_namespace.route('/geometry')
class Geometry(Resource):
	waveguide_args = {
		'data': {
			'cell': {}
		},
		'waveguide_type': str
	}
	@waveguide_namespace.doc('Sets geometry with preview ability')
	@waveguide_namespace.param('waveguide_args', 'Waveguide args')
	@waveguide_namespace.param('preview', 'Preview')
	@waveguides_api.doc(body=waveguide_args)
	def post(self):
		geometry = GeometryModel()
		geometry_parser = geometry.parse_request(waveguide_namespace)
		args = geometry_parser.parse_args()

		if args['preview'] == 1:
			waveguide = Waveguide(waveguides, args['waveguide_type'])
			geometry.waveguide_set(waveguide)

			sim = waveguide.simulate(waveguide.data)

			fig_electric = geometry.waveguide_plot(sim, waveguide)

			waveguide.discard_data()
			waveguide.set_cell(args)
			waveguide.set_geometry()

			cell_preview = geometry.image_render(fig_electric)

			return jsonify(
				cell_preview=cell_preview,
				waveguide=waveguide.__dict__
			)

		return jsonify(
			waveguide='test'
		)


@waveguide_namespace.route('/straight-waveguide')
class StraightWaveguide(Resource):
	@waveguide_namespace.doc('Returns test text and computes of e/m wave propagation in straight waveguide')
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
