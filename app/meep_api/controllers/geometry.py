from flask_restplus import Resource, Namespace, reqparse
from flask import jsonify
from app.meep_api.models.json.geometry import geometry_cell_model

geometry_api = Namespace("geometry", description="Geometry actions")

geometry_model = geometry_api.schema_model('Geometry Model', geometry_cell_model)


@geometry_api.route('/set')
class Set(Resource):
	@geometry_api.doc('Sets cell')
	@geometry_api.expect(geometry_model)
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('coordinates', type=dict)
		parser.add_argument('center', type=dict)
		parser.add_argument('material', type=int)
		args = parser.parse_args()

		return jsonify(
			geometry=args
		)
