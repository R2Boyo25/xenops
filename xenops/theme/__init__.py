import darkdetect

class Theme:
    def __init__(self):
        self.dark_theme: bool = darkdetect.isDark()