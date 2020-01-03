from __future__ import annotations
from os import path
from definitions import root_dir
from typing import Union
import meep as mp
from app.meep_api.models.image_transformer import ImageTransformer
from io import BytesIO
from matplotlib import pyplot, figure


class Waveguide:
	root_dir: str
	dir_out: str
	colormap: str
	sim_data: dict
	waveguide_type: str

	def __init__(self, waveguide_type: str, preview: bool = False):
		if preview:
			waveguide_type = "preview/"+waveguide_type

		self.root_dir = root_dir
		self.dir_out = 'mobile-meep-out/' + waveguide_type
		self.colormap = path.join(self.root_dir, 'app', 'meep_api', 'static', 'colormaps', 'dkbluered')
		self.sim_data = {}
		self.waveguide_type = waveguide_type

	def set_cell(self, args: dict):
		self.sim_data['cell'] = mp.Vector3(args['x'], args['y'], args['z'])

	def get_cell(self) -> object:
		cell = self.sim_data['cell']

		return cell

	def set_geometry(self, args: dict):
		if args['coordinates']['z'] == 0:
			args['coordinates']['z'] = mp.inf

		if self.waveguide_type == 'ninety-degree-bend':
			self.sim_data['geometry'] = [

			]

		self.sim_data['geometry'] = [
			mp.Block(
				mp.Vector3(
					args['coordinates']['x'],
					args['coordinates']['y'],
					args['coordinates']['z']
				),
				center=mp.Vector3(
					args['center']['x'],
					args['center']['y']
				),
				material=mp.Medium(
					epsilon=args['material']
				)
			)
		]

	def set_sources(self, args: dict):
		if not args:
			args['frequency'] = 0.15
			args['center'] = {
				"x": -7,
				"y": 0
			}

		self.sim_data['sources'] = [mp.Source(
			mp.ContinuousSource(frequency=args['frequency']),
			component=mp.Ez,
			center=mp.Vector3(args['center']['x'], args['center']['y']))
		]

	def set_layers(self, args: dict):
		if not args:
			args = 1.0

		self.sim_data['pml_layers'] = [mp.PML(args)]

	def set_resolution(self, args: dict):
		if not args:
			args = 10

		self.sim_data['resolution'] = args

	def simulate(self, data: dict) -> mp.Simulation:
		simulation = mp.Simulation(
			cell_size=data['cell'],
			boundary_layers=data['pml_layers'],
			geometry=data['geometry'],
			sources=data['sources'],
			resolution=data['resolution'])

		return simulation

	def preview_figure(self, simulation: mp.Simulation, waveguide: Waveguide, ) -> figure.Figure:
		eps_data = simulation.get_array(center=mp.Vector3(), size=waveguide.get_cell(), component=mp.Dielectric)
		pyplot.figure()
		pyplot.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
		pyplot.axis('off')
		fig_electric = pyplot.gcf()

		return fig_electric

	def preview_output(self, fig_electric: figure.Figure):
		file = open(self.dir_out+'/preview.png', 'wb+')
		buffer = BytesIO()
		fig_electric.savefig(buffer, format='png')
		buffer.seek(0)
		file.write(buffer.read())
		buffer.close()
		file.close()

		return self.dir_out+'/preview/preview.png'

	def output(self, simulation: mp.Simulation, each: Union[int, float], until: Union[int, float]):
		simulation.use_output_directory(self.dir_out)

		simulation.run(mp.at_every(each, mp.output_png(mp.Ez, "-Zc" + self.colormap)), until=until)

	def image_transform(self, duration: Union[int, float]):
		image_transformer = ImageTransformer(self.dir_out)
		image_transformer.png_to_gif(duration)

	def discard_data(self):
		self.sim_data = {}
