from pathlib import Path

def get_default_images():
    return {
        "sample_puzzle": Path("assets/images/default/sample_puzzle.jpg"),
        "default_icon": Path("assets/images/icons/app_icon.png"),
        "button_icon": Path("assets/images/icons/button_icons.png"),
    }