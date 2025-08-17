import json

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return self.default_config()
        except json.JSONDecodeError:
            return self.default_config()

    def default_config(self):
        return {
            'difficulty': 'medium',
            'background_music': True,
            'sound_effects': True,
            'high_scores': []
        }

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)

    def set_difficulty(self, level):
        self.config_data['difficulty'] = level
        self.save_config()

    def toggle_background_music(self):
        self.config_data['background_music'] = not self.config_data['background_music']
        self.save_config()

    def toggle_sound_effects(self):
        self.config_data['sound_effects'] = not self.config_data['sound_effects']
        self.save_config()

    def add_high_score(self, score):
        self.config_data['high_scores'].append(score)
        self.save_config()