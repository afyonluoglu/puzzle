from pathlib import Path
import os

class ResourceManager:
    def __init__(self):
        self.assets_path = Path(__file__).parent.parent.parent / 'assets'
        self.images_path = self.assets_path / 'images'
        self.audio_path = self.assets_path / 'audio'
        self.fonts_path = self.assets_path / 'fonts'
        self.default_images = self.load_default_images()
        self.background_music = self.load_background_music()

    def load_default_images(self):
        default_images = {}
        default_images_dir = self.images_path / 'default'
        for image_file in default_images_dir.glob('*.jpg'):
            default_images[image_file.stem] = str(image_file)
        return default_images

    def load_background_music(self):
        music_file = self.audio_path / 'background_music.mp3'
        return str(music_file) if music_file.exists() else None

    def get_image(self, image_name):
        image_file = self.images_path / image_name
        return str(image_file) if image_file.exists() else self.default_images.get(image_name)

    def get_sound(self, sound_name):
        sound_file = self.audio_path / sound_name
        return str(sound_file) if sound_file.exists() else None

    def get_font(self, font_name):
        font_file = self.fonts_path / font_name
        return str(font_file) if font_file.exists() else None

    def resource_exists(self, resource_path):
        return os.path.exists(resource_path)