from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkMenu, CTkScrollbar
import os

class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.title("Jigsaw Puzzle Game")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = CTkMenu(self)
        self.config(menu=menu)

        game_menu = CTkMenu(menu)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.start_new_game)
        game_menu.add_command(label="Load Game", command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.quit)

        settings_menu = CTkMenu(menu)
        menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Adjust Settings", command=self.open_settings)

        high_scores_menu = CTkMenu(menu)
        menu.add_cascade(label="High Scores", menu=high_scores_menu)
        high_scores_menu.add_command(label="View High Scores", command=self.view_high_scores)

    def create_widgets(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = CTkLabel(self.main_frame, text="Welcome to the Jigsaw Puzzle Game!", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.start_button = CTkButton(self.main_frame, text="Start Game", command=self.start_new_game)
        self.start_button.pack(pady=10)

        self.load_button = CTkButton(self.main_frame, text="Load Game", command=self.load_game)
        self.load_button.pack(pady=10)

        self.settings_button = CTkButton(self.main_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)

        self.high_scores_button = CTkButton(self.main_frame, text="High Scores", command=self.view_high_scores)
        self.high_scores_button.pack(pady=10)

        self.scrollbar = CTkScrollbar(self.main_frame)
        self.scrollbar.pack(side="right", fill="y")

    def start_new_game(self):
        print("Starting a new game...")

    def load_game(self):
        print("Loading a saved game...")

    def open_settings(self):
        print("Opening settings...")

    def view_high_scores(self):
        print("Viewing high scores...")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()