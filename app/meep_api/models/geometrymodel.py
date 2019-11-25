import matplotlib.pyplot as plt
from app.meep_api.models.waveguide import Waveguide
import meep as mp
import io


class GeometryModel:
	def parse_request(self, namespace: object):
		parser = namespace.parser()
		parser.add_argument('waveguide', type=object, location='form', help='Waveguide object')

		return parser

	def waveguide_set(self, waveguide: Waveguide):
		waveguide.set_geometry()
		waveguide.set_sources()
		waveguide.set_layers()
		waveguide.set_resolution()

	def waveguide_plot(self, sim: mp.Simulation, waveguide: Waveguide):
		eps_data = sim.get_array(center=mp.Vector3(), size=waveguide.get_cell(), component=mp.Dielectric)
		plt.figure()
		plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
		plt.axis('off')
		fig_electric = plt.gcf()

		return fig_electric

	def image_render(self, fig_electric: plt.gcf()):
		buffer = io.BytesIO()
		fig_electric.savefig(buffer, format='png')
		buffer.seek(0)
		cell_preview = buffer.read()
		buffer.close()

		return cell_preview
