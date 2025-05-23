import customtkinter as ctk
from PIL import Image, ImageTk
import os
from VIEWS.colors import COLORS


class Sidebar:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master, fg_color=COLORS.card, width=220, corner_radius=0)
        self.frame.pack(side="left", fill="y")
        self.frame.pack_propagate(False)
        
        # App logo/title
        logo_frame = ctk.CTkFrame(self.frame, fg_color="transparent", height=60)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        try:
            icon_image = Image.open("./Sources/iconoo.jpg")
            icon_image = icon_image.resize((40, 30))
            icon_ctk = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(40, 30))
            
            icon_label = ctk.CTkLabel(logo_frame, image=icon_ctk, text="")
            icon_label.pack(side="left", padx=(20, 10))
        except Exception as e:
            print(f"Error loading sidebar icon: {e}")
        
        ctk.CTkLabel(
            logo_frame, text="Smartgrow", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS.primary
        ).pack(side="left")
        
        # Navigation menu
        self.nav_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=20)
        
        self.nav_items = [
            {"icon": "🏠", "text": "Home", "view": "home"},
            {"icon": "📊", "text": "History", "view": "history"},
            {"icon": "🔔", "text": "Notify", "view": "notifications"},
            {"icon": "⚙️", "text": "Settings", "view": "custom"}
        ]
        
        self.nav_buttons = []
        for item in self.nav_items:
            button = self.create_nav_button(item["icon"], item["text"], item["view"])
            self.nav_buttons.append(button)
        
        # Set the first button as active
        self.set_active_button(self.nav_buttons[0])
        
    def create_nav_button(self, icon, text, view):
        button = ctk.CTkButton(
            self.nav_frame,
            text=f"{icon}  {text}",
            anchor="w",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            text_color=COLORS.text_light,
            hover_color="#F3F4F6",
            font=ctk.CTkFont(size=14),
            command=lambda v=view: self.on_nav_click(v)
        )
        button.pack(pady=5, padx=20)
        button.view = view
        return button
    
    def set_active_button(self, active_button):
        # Reset all buttons
        for button in self.nav_buttons:
            button.configure(
                fg_color="transparent",
                text_color=COLORS.text_light
            )
        
        # Set active button
        active_button.configure(
            fg_color=COLORS.primary,
            text_color="white"
        )
    
    def on_nav_click(self, view):
        # Find the button for this view
        for button in self.nav_buttons:
            if button.view == view:
                self.set_active_button(button)
                break
        
        # Show the corresponding view in main content
        if hasattr(self, 'main_content'):
            self.main_content.show_view(view)