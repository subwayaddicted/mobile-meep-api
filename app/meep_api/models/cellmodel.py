class CellModel:
	def parse_request(self, namespace: object):
		parser = namespace.parser()
		parser.add_argument('waveguide_data', type=list, location='json', help='waveguide type')

		return parser
