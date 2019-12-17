import os
from flask import Blueprint, jsonify, request
from flask_restplus import Api, Resource, fields
import meep as mp
from app.meep_api.models.image_transformer import ImageTransformer
from app.meep_api.models.waveguide import Waveguide
from app.meep_api.models.json.waveguide import waveguide_json_model


waveguides = Blueprint('waveguides', __name__)

waveguides_api = Api(waveguides, version='0.3.0', title='meep API waveguides', description='waveguides API')
waveguide_namespace = waveguides_api.namespace('waveguides', description='Simple waveguides endpoints')
cell_data = waveguide_namespace.schema_model('waveguide_data', waveguide_json_model)


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

# @waveguide_namespace.route('/ninety-degree-bend')
# class NinetyDegreeBend(Resource):
# 	@waveguide_namespace.doc('Returns test text and computes of e/m wave propagation in 90 degree bend waveguide')
# 	def get(self):
# 		root_dir = os.path.dirname(waveguides.root_path)
# 		dir_out = 'mobile-meep-out/ninety-degree-bend'
# 		colormap = os.path.join(root_dir, 'static', 'colormaps', 'dkbluered')
#
# 		cell = mp.Vector3(16, 16, 0)
# 		geometry = [mp.Block(
# 			mp.Vector3(12, 1, mp.inf),
# 			center=mp.Vector3(-2.5, -3.5),
# 			material=mp.Medium(epsilon=12)),
# 			mp.Block(
# 				mp.Vector3(1, 12, mp.inf),
# 				center=mp.Vector3(3.5, 2),
# 				material=mp.Medium(epsilon=12))]
#
# 		pml_layers = [mp.PML(1.0)]
#
# 		resolution = 10
#
# 		sources = [mp.Source(
# 			mp.ContinuousSource(wavelength=2 * (11 ** 0.5), width=20),
# 			component=mp.Ez,
# 			center=mp.Vector3(-7, -3.5),
# 			size=mp.Vector3(0, 1))]
#
# 		sim = mp.Simulation(
# 			cell_size=cell,
# 			boundary_layers=pml_layers,
# 			geometry=geometry,
# 			sources=sources,
# 			resolution=resolution)
#
# 		sim.use_output_directory(dir_out)
#
# 		sim.run(mp.at_every(0.6, mp.output_png(mp.Ez, "-Zc" + colormap)), until=200)
#
# 		image_transformer = ImageTransformer(dir_out)
# 		image_transformer.png_to_gif()
#
# 		gif_path = dir_out + '-' + 'movie.gif'
# 		gif = open(gif_path, 'rb')
# 		gif_encoded = base64.b64encode(gif.read()).decode()
#
# 		return jsonify(
# 			electric='gif_encoded'
# 		)
