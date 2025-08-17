from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkScrollbar
import sqlite3

class HighScoresScreen(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        self.create_widgets()
        self.load_high_scores()

    def create_widgets(self):
        self.title_label = CTkLabel(self, text="High Scores", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.score_list_frame = CTkFrame(self)
        self.score_list_frame.pack(pady=10)

        self.score_listbox = CTkScrollbar(self.score_list_frame)
        self.score_listbox.pack(side="right", fill="y")

        self.score_display = CTkLabel(self.score_list_frame, text="", anchor="w", justify="left")
        self.score_display.pack(side="left", fill="both")

        self.back_button = CTkButton(self, text="Back", command=self.master.show_main_menu)
        self.back_button.pack(pady=10)

    def load_high_scores(self):
        conn = sqlite3.connect('data/high_scores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, score FROM high_scores ORDER BY score DESC LIMIT 10")
        high_scores = cursor.fetchall()
        conn.close()

        score_text = ""
        for idx, (name, score) in enumerate(high_scores):
            score_text += f"{idx + 1}. {name}: {score}\n"

        self.score_display.configure(text=score_text)