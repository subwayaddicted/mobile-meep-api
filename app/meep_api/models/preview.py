from meep import Simulation, Vector3, Dielectric
from matplotlib import pyplot, figure
from io import BytesIO
from app.meep_api.models.waveguide import Waveguide


class Preview:
	simulation: Simulation
	waveguide: Waveguide

	def __init__(self, simulation: Simulation, waveguide: Waveguide):
		"""

		:param simulation:
		:param waveguide:
		"""
		self.simulation = simulation
		self.waveguide = waveguide

	def preview_figure(self) -> figure.Figure:
		"""

		:return:
		"""
		eps_data = self.simulation.get_array(center=Vector3(), size=self.waveguide.get_cell(), component=Dielectric)
		pyplot.figure()
		pyplot.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
		pyplot.axis('off')
		fig_electric = pyplot.gcf()

		return fig_electric

	def preview_output(self, fig_electric: figure.Figure) -> str:
		"""

		:param fig_electric:
		:return: string with path to preview picture
		"""
		file = open(self.waveguide.dir_out + '/preview.png', 'wb+')
		buffer = BytesIO()
		fig_electric.savefig(buffer, format='png')
		buffer.seek(0)
		file.write(buffer.read())
		buffer.close()
		file.close()

		return self.waveguide.dir_out + '/preview/preview.png'
