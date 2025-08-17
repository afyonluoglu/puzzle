from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkCanvas
from tkinter import PhotoImage
import os

class GameScreen(CTkFrame):
    def __init__(self, master, puzzle_board, piece_tray, on_hint, on_save, on_exit):
        super().__init__(master)
        self.master = master
        self.puzzle_board = puzzle_board
        self.piece_tray = piece_tray
        self.on_hint = on_hint
        self.on_save = on_save
        self.on_exit = on_exit
        
        self.setup_ui()

    def setup_ui(self):
        self.canvas = CTkCanvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.puzzle_board_frame = CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.puzzle_board_frame, anchor="nw")

        self.piece_tray_frame = CTkFrame(self.canvas)
        self.canvas.create_window((0, self.puzzle_board_frame.winfo_height()), window=self.piece_tray_frame, anchor="nw")

        self.hint_button = CTkButton(self, text="Hint", command=self.on_hint)
        self.hint_button.pack(side="left", padx=10, pady=10)

        self.save_button = CTkButton(self, text="Save", command=self.on_save)
        self.save_button.pack(side="left", padx=10, pady=10)

        self.exit_button = CTkButton(self, text="Exit", command=self.on_exit)
        self.exit_button.pack(side="right", padx=10, pady=10)

        self.update_ui()

    def update_ui(self):
        # Update the puzzle board and piece tray UI elements
        self.puzzle_board_frame.update()
        self.piece_tray_frame.update()

    def load_image(self, image_path):
        if os.path.exists(image_path):
            self.image = PhotoImage(file=image_path)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def clear(self):
        self.canvas.delete("all")