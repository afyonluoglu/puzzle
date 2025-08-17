import customtkinter as ctk
from app import App

def main():
    # Initialize the main application
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Create the main window
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()