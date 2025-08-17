from customtkinter import CTkTheme

class AppTheme:
    def __init__(self):
        self.theme = CTkTheme()

    def set_light_theme(self):
        self.theme.set_color("bg_color", "#FFFFFF")
        self.theme.set_color("text_color", "#000000")
        self.theme.set_color("button_color", "#007BFF")
        self.theme.set_color("button_hover_color", "#0056b3")
        self.theme.set_color("highlight_color", "#FFD700")

    def set_dark_theme(self):
        self.theme.set_color("bg_color", "#2E2E2E")
        self.theme.set_color("text_color", "#FFFFFF")
        self.theme.set_color("button_color", "#1E90FF")
        self.theme.set_color("button_hover_color", "#1C86EE")
        self.theme.set_color("highlight_color", "#FFD700")

    def apply_theme(self, window):
        window.configure(bg=self.theme.get_color("bg_color"))
        for widget in window.winfo_children():
            widget.configure(bg=self.theme.get_color("bg_color"), fg=self.theme.get_color("text_color"))