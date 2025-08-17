from customtkinter import CTkButton, CTkLabel, CTkFrame, CTkEntry, CTkOptionMenu

class CustomButton(CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="lightblue", hover_color="blue")

class CustomLabel(CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(text_color="black")

class CustomEntry(CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_color="gray")

class CustomOptionMenu(CTkOptionMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="lightgray", dropdown_fg_color="white")