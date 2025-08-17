from playsound import playsound
import os
import threading
import pygame

class AudioManager:
    def __init__(self):
        self.audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio")
        self.background_music_path = os.path.join(self.audio_dir, "background_music.mp3")
        self.effects_dir = os.path.join(self.audio_dir, "sound_effects")
        
        # Create directories if they don't exist
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.effects_dir, exist_ok=True)
        
        # Sound effect paths
        self.sound_effects = {
            'piece_placed': os.path.join(self.effects_dir, "piece_placed.mp3"),
            'level_complete': os.path.join(self.effects_dir, "level_complete.mp3"),
            'hint_used': os.path.join(self.effects_dir, "hint_used.mp3")
        }
        
        # Check if files exist
        self._create_placeholder_files()
        pygame.mixer.init()        
        self.background_music_playing = False
    
    def _create_placeholder_files(self):
        """Create placeholder audio files if they don't exist"""
        # For now, just check if they exist - in a real game you'd include actual audio files
        if not os.path.exists(self.background_music_path):
            print(f"Warning: Background music file not found at {self.background_music_path}")
            
        for effect_name, effect_path in self.sound_effects.items():
            if not os.path.exists(effect_path):
                print(f"Warning: Sound effect '{effect_name}' not found at {effect_path}")
    
    def play_background_music(self):
        """Play background music in a loop"""
        if os.path.exists(self.background_music_path):
            try:
                pygame.mixer.music.load(self.background_music_path)
                pygame.mixer.music.play(-1)  # Loop
                self.background_music_playing = True
            except Exception as e:
                print(f"Error playing background music: {e}")
        else:
            print("Background music file not found. Continuing without music.")
    
    def _play_music_thread(self):
        """Thread for playing background music"""
        while self.background_music_playing:
            try:
                playsound(self.background_music_path)
                # If we get here, the music finished playing
                if not self.background_music_playing:
                    break
            except Exception as e:
                print(f"Error in music thread: {e}")
                break
    
    def stop_background_music(self):
        """Stop the background music"""
        if self.background_music_playing:
            pygame.mixer.music.stop()
            self.background_music_playing = False
            # print("✅ Background music stopped.")

    def play_sound_effect(self, effect_name):
        """Play a sound effect"""
        if effect_name in self.sound_effects:
            effect_path = self.sound_effects[effect_name]
            if os.path.exists(effect_path):
                try:
                    # Play in a separate thread
                    threading.Thread(target=lambda: playsound(effect_path), daemon=True).start()
                except Exception as e:
                    print(f"Error playing sound effect: {e}")
            else:
                print(f"Sound effect file not found: {effect_path}")
        else:
            print(f"Unknown sound effect: {effect_name}")