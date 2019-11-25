class CellModel:
	def parse_request(self, namespace: object):
		parser = namespace.parser()
		parser.add_argument('preview', type=int, location='args', help='Whether render preview or not')
		parser.add_argument('z', type=int, location='args', help='z')
		parser.add_argument('y', type=int, location='args', help='y')
		parser.add_argument('x', type=int, location='args', help='x')

		return parser
