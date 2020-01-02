from flask_restplus import Resource, Namespace, reqparse
from flask import jsonify
from app.meep_api.models.json.cell import cell_json_model

cell_api = Namespace("cell", description="Cell actions")

cell_model = cell_api.schema_model('Cell Model', cell_json_model)


@cell_api.route('/set', methods=["post"])
class Set(Resource):
	@cell_api.doc('Sets cell')
	@cell_api.expect(cell_model)
	@cell_api.param('waveguide_type', 'Describing waveguide type selected at the beginning')
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('x', type=int)
		parser.add_argument('y', type=int)
		parser.add_argument('z', type=int)
		parser.add_argument('waveguide_type', type=str)
		args = parser.parse_args()

		waveguide_type = args['waveguide_type']
		del args['waveguide_type']

		return jsonify(
			cell=args,
			waveguide_type=waveguide_type
		)
