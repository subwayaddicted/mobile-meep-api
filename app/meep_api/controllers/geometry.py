from flask_restplus import Resource, Namespace, reqparse
from flask import jsonify
from app.meep_api.models.waveguide import Waveguide
from app.meep_api.models.json.geometry import geometry_json_model
from app.meep_api.models.preview import Preview as GeometryPreview

geometry_api = Namespace("geometry", description="Geometry actions")

geometry_model = geometry_api.schema_model('Geometry Model', geometry_json_model)


@geometry_api.route('/set')
class Set(Resource):
	@geometry_api.doc('Sets geometry for straight waveguide')
	@geometry_api.expect(geometry_model)
	@geometry_api.param('waveguide_type', 'Describing waveguide type selected at the beginning')
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('coordinates', type=dict)
		parser.add_argument('center', type=dict)
		parser.add_argument('material', type=int)
		parser.add_argument('waveguide_type', type=str)
		args = parser.parse_args()

		waveguide_type = args['waveguide_type']
		del args['waveguide_type']

		return jsonify(
			geometry=args,
			waveguide_type=waveguide_type
		)


@geometry_api.route('/preview')
class Preview(Resource):
	"""
	Example json:
	coordinates: bigger than 16, 1, 0(inf basically)
	center: 0, 0
	material: 12
	"""
	@geometry_api.doc('Sets geometry for straight waveguide')
	@geometry_api.expect(geometry_model)
	@geometry_api.param('waveguide_type', 'Describing waveguide type selected at the beginning')
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('coordinates', type=dict)
		parser.add_argument('center', type=dict)
		parser.add_argument('material', type=int)
		parser.add_argument('waveguide_type', type=str)
		args = parser.parse_args()

		waveguide_type = args['waveguide_type']
		del args['waveguide_type']

		waveguide = Waveguide(waveguide_type, True)
		cell = {"x": 16, "y": 8, "z": 0}
		waveguide.set_cell(cell)
		waveguide.set_geometry(args)
		waveguide.set_sources({})
		waveguide.set_layers({})
		waveguide.set_resolution({})

		sim = waveguide.simulate(waveguide.sim_data)
		sim.run(until=1)

		preview = GeometryPreview(sim, waveguide)

		fig = preview.preview_figure()
		output = preview.preview_output(fig)

		return jsonify(
			fig=output
		)
