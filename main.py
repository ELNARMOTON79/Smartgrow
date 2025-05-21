import customtkinter as ctk
from PIL import Image, ImageTk
import os
from VIEWS.sidebar import Sidebar
from VIEWS.maincontent import MainContent
from VIEWS.colors import COLORS



# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Smartgrow - Sistema hidroponía")
        self.geometry("1200x700")
        self.minsize(900, 600)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        
        # Create main content

        self.main_content = MainContent(self)
        
        # Connect sidebar to main content
        self.sidebar.main_content = self.main_content

if __name__ == "__main__":
    app = App()
    app.mainloop()