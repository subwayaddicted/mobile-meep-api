from flask_restplus import Resource, Namespace
from flask import jsonify
from app.meep_api.models.cellmodel import CellModel
from app.meep_api.models.json.cell import cell_json_model


cell_api = Namespace("cell", description="Cell actions")

cell_data = cell_api.schema_model('cell_data', cell_json_model)


@cell_api.route('/preview', methods=["post"])
class Cell(Resource):
	@cell_api.doc('Sets cell')
	@cell_api.marshal_with(cell_data, mask="data{cell{x}}, data{cell{y}}, data{cell{z}}")
	def post(self):
		cell_model = CellModel()
		cell_parser = cell_model.parse_request(cell_api)
		args = cell_parser.parse_args()

		cell_args = {
			'cell': {
				'x': 'test',
				'y': 'test',
				'z': 'test'
			}
		}

		for arg in args:
			cell_args['cell'][arg] = args[arg]

		return jsonify(
			waveguide_args=cell_args
		)
