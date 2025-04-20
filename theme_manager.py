# theme_manager.py

LIGHT_THEME = {
    "navbar_bg": "#3CB371",
    "button_fg": "#4A90E2",
    "text_color": "#000000",
    "bg_color": "#FFFFFF",
    "accent": "#A6E6CF"
}

DARK_THEME = {
    "navbar_bg": "#6FC997",
    "button_fg": "#11E3A5F",
    "text_color": "#FFFFFF",
    "bg_color": "#000000",
    "accent": "#B0BEC5"
}

class ThemeManager:
    current_theme = "light"  # Cambia a "dark" si quieres iniciar en oscuro
    themes = {"light": LIGHT_THEME, "dark": DARK_THEME}
    subscribers = []  # Widgets que escuchan el cambio de tema

    @classmethod
    def get_color(cls, key):
        return cls.themes[cls.current_theme][key]

    @classmethod
    def toggle_theme(cls):
        cls.current_theme = "dark" if cls.current_theme == "light" else "light"
        for widget in cls.subscribers:
            widget.apply_theme()

    @classmethod
    def subscribe(cls, widget):
        cls.subscribers.append(widget)
