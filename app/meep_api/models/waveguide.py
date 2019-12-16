import os
from typing import Union
import meep as mp
from app.meep_api.models.image_transformer import ImageTransformer


class Waveguide:
	root_dir: str
	dir_out: str
	colormap: str
	data: dict

	def __init__(self, namespace: object, waveguide_type: str):
		self.root_dir = os.path.dirname(namespace.root_path)
		self.dir_out = 'mobile-meep-out/' + waveguide_type
		self.colormap = os.path.join(self.root_dir, 'static', 'colormaps', 'dkbluered')
		self.data = {}

	def set_cell(self):
		self.data['cell'] = mp.Vector3(16, 8, 0)

	def set_geometry(self):
		self.data['geometry'] = [
			mp.Block(
				mp.Vector3(mp.inf, 1, mp.inf),
				center=mp.Vector3(),
				material=mp.Medium(epsilon=12))
		]

	def set_sources(self):
		self.data['sources'] = [mp.Source(
			mp.ContinuousSource(frequency=0.15),
			component=mp.Ez,
			center=mp.Vector3(-7, 0))
		]

	def set_layers(self):
		self.data['pml_layers'] = [mp.PML(1.0)]

	def set_resolution(self):
		self.data['resolution'] = 10

	def simulate(self, data: dict) -> object:
		simulation = mp.Simulation(
			cell_size=data['cell'],
			boundary_layers=data['pml_layers'],
			geometry=data['geometry'],
			sources=data['sources'],
			resolution=data['resolution'])

		return simulation

	def output(self, simulation: object, each: Union[int, float], until: Union[int, float]):
		simulation.use_output_directory(self.dir_out)

		simulation.run(mp.at_every(each, mp.output_png(mp.Ez, "-Zc" + self.colormap)), until=until)

	def image_transform(self, duration: Union[int, float]):
		image_transformer = ImageTransformer(self.dir_out)
		image_transformer.png_to_gif(duration)
