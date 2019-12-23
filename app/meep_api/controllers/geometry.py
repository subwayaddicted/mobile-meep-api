from flask_restplus import Resource, Namespace, reqparse
from flask import jsonify
from app.meep_api.models.waveguide import Waveguide
from app.meep_api.models.json.geometry import geometry_cell_model

geometry_api = Namespace("geometry", description="Geometry actions")

geometry_model = geometry_api.schema_model('Geometry Model', geometry_cell_model)


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
		cell = {"x": args["coordinates"]["x"], "y": args["coordinates"]["y"], "z": args["coordinates"]["z"]}
		waveguide.set_cell(cell)
		waveguide.set_geometry(args)
		waveguide.set_sources({})
		waveguide.set_layers({})
		waveguide.set_resolution({})

		sim = waveguide.simulate(waveguide.sim_data)
		sim.run(until=1)
		fig = waveguide.preview_figure(sim, waveguide)
		output = waveguide.preview_output(fig)

		return jsonify(
			fig=output
		)
