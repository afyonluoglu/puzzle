import pickle
import os
import time

from tkinter import * 
from tkinter.simpledialog import askstring 
from tkinter import filedialog

class SaveManager:
    def __init__(self, parent, save_dir="saves"):
        self.parent = parent
        self.save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), save_dir)
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_file = os.path.join(self.save_dir, "game_save.pkl")
    
    def sm_save_game(self, game_data):
        if self.parent.current_save_file:
            name = self.parent.current_save_file
            self.save_file = name
            print(f"Saving game to existing file: {self.save_file}")
        else:
            # Ask user for a name if not already set
            name = askstring('Oyun saklama', 'Dosya Adı:') 
            self.save_file = os.path.join(self.save_dir, f"{name}.pkl")         
            print(f"Saving game to new file: {self.save_file}")   
        
        if name:
            """Save game data to file"""
            # Add timestamp
            game_data['timestamp'] = time.time()
            
            with open(self.save_file, 'wb') as f:
                pickle.dump(game_data, f)
            self.parent.show_message(f"💾 Game saved as {self.save_file} successfully!")
            print(f"💾 Game saved as {self.save_file}")
            return True
    
    def load_game(self, game_file):
        """Load game data from file"""
        
        print(f"🔄 Loading game from file: {game_file}")
        if game_file:
            print(f"Selected folder: {game_file}")
            self.save_file = game_file
            if not os.path.exists(self.save_file):
                return None
            
            try:
                with open(self.save_file, 'rb') as f:
                    game_data = pickle.load(f)
                return game_data
            except Exception as e:
                print(f"Error loading game {self.save_file}: {e}")
                return None

