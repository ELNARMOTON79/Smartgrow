import customtkinter as ctk
from VIEWS.sidebar import Sidebar
from VIEWS.main_content import MainContent

class SmartGrowApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.geometry("1000x600")
        self.app.title("SmartGrow")
        self.app.configure(fg_color="#FFFFFF")

        self.sidebar = Sidebar(self.app, None)
        self.main_content = MainContent(self.app)
        self.sidebar.main_content = self.main_content

    def run(self):
        self.app.mainloop()
