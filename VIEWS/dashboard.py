import customtkinter as ctk
from PIL import Image, ImageTk
import os
from VIEWS.colors import COLORS

class Dashboard:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        
        # Stats section
        stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_data = [
            {"title": "Temperatura", "value": "22.5°C", "icon": " 🌡️", "color": COLORS.primary},
            {"title": "pH", "value": "6.2", "icon": "🧪", "color": COLORS.secondary},
            {"title": "Conductividad", "value": "1300 µS/cm", "icon": "⚡", "color": "#F59E0B"},
            {"title": "Water Level", "value": "100%", "icon": "🚰", "color": "#F59E0B"}
        ]
        
        # Create stats cards in a row
        for i, stat in enumerate(stats_data):
            card = self._create_card(stats_frame, stat["title"], stat["value"], stat["icon"], stat["color"])
            card.pack(side="left", fill="x", expand=True, padx=5)
        
        # Image container
        image_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        image_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.image_label = ctk.CTkLabel(image_container, text="")
        self.image_label.pack(fill="both", expand=True)
        self.frame.bind("<Configure>", self._resize_image)
        
        # Try to load the background image
        self.tk_image = None
        self.original_image = None
        image_path = "./Sources/fondo_light.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color=COLORS.danger)

    def _create_card(self, parent, title, value, icon, color):
        """Helper to create a stat card"""
        card = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=10, border_width=1, border_color=COLORS.border)
        
        # Icon with background
        icon_bg = ctk.CTkFrame(card, width=36, height=36, fg_color=color, corner_radius=18)
        icon_bg.pack(side="left", padx=15, pady=15)
        icon_bg.pack_propagate(False)
        
        ctk.CTkLabel(icon_bg, text=icon, font=ctk.CTkFont(size=16), text_color="white").pack(expand=True)
        
        # Text content
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
        
        ctk.CTkLabel(
            text_frame, text=value, font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame, text=title, font=ctk.CTkFont(size=14),
            text_color=COLORS.text_light
        ).pack(anchor="w")
        
        return card
        
    def _resize_image(self, event):
        if hasattr(self, 'original_image') and self.original_image:
            resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.configure(image=self.tk_image)