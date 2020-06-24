from flask_restplus import Api
from app.meep_api.controllers.cell import cell_api
from app.meep_api.controllers.geometry import geometry_api
from app.meep_api.controllers.waveguides import waveguide_api


api = Api(
    title='Meep API',
    version='0.4.0',
    description='Project for university',
)

api.add_namespace(cell_api)
api.add_namespace(geometry_api)
api.add_namespace(waveguide_api)
