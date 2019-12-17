from flask_restplus import Resource, Namespace
from flask import jsonify
from app.meep_api.models.geometrymodel import GeometryModel
from app.meep_api.models.json.geometry import geometry_cell_model


geometry_api = Namespace("geometry", description="Geometry actions")

geometry_data = geometry_api.schema_model('geometry_data', geometry_cell_model)


@geometry_api.route('/preview')
class Geometry(Resource):
	@geometry_api.doc('Sets geometry with preview ability')
	@geometry_api.marshal_with(geometry_cell_model, mask="x, y, z")
	def post(self):
		geometry = GeometryModel()
		geometry_parser = geometry.parse_request(geometry_api)
		args = geometry_parser.parse_args()

		geometry_args = {
			'geometry': {
				'coordinates': {
					'x',
					'y',
					'z'
				},
				'center': {
					'x',
					'y'
				},
				'material': int
			}
		}

		for arg in args:
			geometry_args['geometry'] = args[arg]

		return jsonify(
			waveguide_args=geometry_args
		)