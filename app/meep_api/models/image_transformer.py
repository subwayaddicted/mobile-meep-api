import os
import imageio


class ImageTransformer:

    def __init__(self, dir_out):
        self.png_dir = dir_out
        self.images = []
        self.gif_dir = dir_out + '-' + 'movie.gif'

    def png_to_gif(self, duration):
        for file_name in os.listdir(self.png_dir):
            if file_name.endswith('.png'):
                file_path = os.path.join(self.png_dir, file_name)
                self.images.append(imageio.imread(file_path))
        imageio.mimsave(self.gif_dir, self.images, format='GIF', duration=duration)
