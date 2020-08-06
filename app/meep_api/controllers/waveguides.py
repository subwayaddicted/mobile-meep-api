from flask import Blueprint, jsonify
from flask_restplus import Resource, Namespace, reqparse
from app.meep_api.models.waveguide import Waveguide
from app.meep_api.models.json.waveguide import waveguide_json_model


waveguides = Blueprint('waveguides', __name__)

waveguide_api = Namespace('waveguides', description='Simple waveguides endpoints')
waveguide_model = waveguide_api.schema_model('Waveguide Model', waveguide_json_model)


@waveguide_api.route('/straight-waveguide')
class StraightWaveguide(Resource):
	@waveguide_api.doc('Returns test text and computes of e/m wave propagation in straight waveguide')
	@waveguide_api.expect(waveguide_model)
	@waveguide_api.param('waveguide_type', 'Describing waveguide type selected at the beginning')
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('data', type=dict)
		parser.add_argument('waveguide_type', type=str)
		args = parser.parse_args()

		waveguide_type = 'straight'#args['waveguide_type']
		del args['waveguide_type']

		data = args['data']
		time = data['simulation_time']

		waveguide = Waveguide(waveguide_type, False)

		waveguide.set_cell(data['cell'])
		waveguide.set_geometry(data['geometry'])
		waveguide.set_sources(data['sources'])
		waveguide.set_layers(data['pml_layers'])
		waveguide.set_resolution(data['resolution'])

		sim = waveguide.simulate(waveguide.sim_data)
		waveguide.output(sim, time['between'], time['until'])
		waveguide.image_transform(time['between'])

		folder = 'mobile-meep-out/'+waveguide_type
		self.remove_pngs(folder)

		return jsonify(
			electric='mobile-meep-out/'+waveguide_type+'-movie.gif'
		)

# @waveguide_api.route('/ninety-degree-bend')
# class NinetyDegreeBend(Resource):
# 	@waveguide_api.doc('Returns test text and computes of e/m wave propagation in 90 degree bend waveguide')
# 	def get(self):
# 		root_dir = os.path.dirname(waveguides.root_path)
# 		dir_out = 'mobile-meep-out/ninety-degree-bend'
# 		colormap = os.path.join(root_dir, 'static', 'colormaps', 'dkbluered')
#
# 		cell = mp.Vector3(16, 16, 0)
# 		geometry = [
# 			mp.Block(
# 				mp.Vector3(12, 1, mp.inf),
# 				center=mp.Vector3(-2.5, -3.5),
# 				material=mp.Medium(epsilon=12)),
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
