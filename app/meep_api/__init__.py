from flask_restplus import Api
from app.meep_api.controllers.cell import cell_api
from app.meep_api.controllers.geometry import geometry_api


api = Api(
    title='Meep API',
    version='0.1.0',
    description='Project for university',
)

api.add_namespace(cell_api)
api.add_namespace(geometry_api)
