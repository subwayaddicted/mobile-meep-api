import os
import shutil


class FolderManager:
	folder: str

	def __init__(self, folder: str):
		"""
		Constructor

		:param folder: path to folder
		"""
		self.folder = folder

	def remove_pngs(self):
		"""
		Removes png's generated to make gif
		"""
		for filename in os.listdir(self.folder):
			file_path = os.path.join(self.folder, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))
