import customtkinter as ctk
from PIL import Image, ImageTk
import os

class MainContent:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master=master, fg_color="#FFFFFF")
        self.frame.pack(side="left", fill="both", expand=True)

        self.content_container = ctk.CTkFrame(master=self.frame, fg_color="#FFFFFF")
        self.content_container.pack(fill="both", expand=True)

        self.views = {}
        self.tk_image = None
        self.original_image = None

        self._create_views()
        self.show_view("home")

    def _create_views(self):
        home_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        self.image_label = ctk.CTkLabel(home_frame, text="")
        self.image_label.pack(fill="both", expand=True)
        home_frame.bind("<Configure>", self._resize_image)
        self.views["home"] = home_frame

        image_path = "./Sources/fondo_light.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color="red")

        history_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(history_frame, text="Historial", font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["history"] = history_frame

        notif_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(notif_frame, text="Notificaciones", font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["notifications"] = notif_frame

        custom_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        self.custom_label = ctk.CTkLabel(custom_frame, text="", font=ctk.CTkFont(size=20))
        self.custom_label.pack(pady=20)
        self.views["custom"] = custom_frame

    def _resize_image(self, event):
        if self.original_image:
            resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.configure(image=self.tk_image)

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()
        if view_name in self.views:
            self.views[view_name].pack(fill="both", expand=True)

    def show_custom_view(self, text):
        self.custom_label.configure(text=text)
        self.show_view("custom")
