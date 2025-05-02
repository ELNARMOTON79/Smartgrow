import customtkinter as ctk

class Sidebar:
    def __init__(self, master, main_content):
        self.main_content = main_content
        self.frame = ctk.CTkFrame(master=master, width=200, corner_radius=0, fg_color="#A6E6CF")
        self.frame.pack(side="left", fill="y")

        self._create_widgets()

    def _create_widgets(self):
        title_label = ctk.CTkLabel(master=self.frame, 
                                   text="SmartGrow", 
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="#3CB371")
        title_label.pack(pady=(20, 10))

        ctk.CTkLabel(master=self.frame, text="", fg_color="#A6E6CF").pack(pady=(0, 30))

        ctk.CTkButton(master=self.frame, 
                      text="Home",
                      command=lambda: self.main_content.show_view("home"),
                      fg_color="#4A90E2",
                      hover_color="#3CB371",
                      text_color="#FFFFFF").pack(pady=10, padx=20, fill="x")

        self.graphics_menu = ctk.CTkOptionMenu(
            master=self.frame,
            values=["Ph", "Temperature", "Conductivity", "Water Level"],
            anchor="w",
            command=self.handle_graphics,
            fg_color="#4A90E2",
            button_color="#4A90E2",
            button_hover_color="#3CB371",
            text_color="#FFFFFF"
        )
        self.graphics_menu.set("Graphics")
        self.graphics_menu.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(master=self.frame, 
                      text="History",
                      command=lambda: self.main_content.show_view("history"),
                      fg_color="#4A90E2",
                      hover_color="#3CB371",
                      text_color="#FFFFFF").pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(master=self.frame, 
                      text="Notifications",
                      command=lambda: self.main_content.show_view("notifications"),
                      fg_color="#4A90E2",
                      hover_color="#3CB371",
                      text_color="#FFFFFF").pack(pady=10, padx=20, fill="x")

        self.settings_menu = ctk.CTkOptionMenu(
            master=self.frame,
            values=["Inside", "Outside"],
            anchor="w",
            command=self.handle_settings,
            fg_color="#4A90E2",
            button_color="#4A90E2",
            button_hover_color="#3CB371",
            text_color="#FFFFFF"
        )
        self.settings_menu.set("Settings")
        self.settings_menu.pack(pady=10, padx=20, fill="x")

    def handle_graphics(self, value):
        self.graphics_menu.set("Graphics")
        self.main_content.show_custom_view(f"Graphic: {value}")

    def handle_settings(self, value):
        self.settings_menu.set("Settings")
        self.main_content.show_custom_view(f"Settings: {value}")
