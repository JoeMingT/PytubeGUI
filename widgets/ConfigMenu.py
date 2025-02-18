import customtkinter as ctk

class ConfigMenu(ctk.CTkFrame):
    def __init__(self, app, video_obj):
        super().__init__(app)
        self.app = app
        self.yt = video_obj
        
        self.config_menu_frame = ctk.CTkFrame(app, fg_color="transparent")
        self.config_menu_frame.pack(padx=20, pady=20)
        
        self.heading_label = ctk.CTkLabel(self.config_menu_frame, text="Testing", font=self.app.h1)
        self.heading_label.grid(column=0, row=0, columnspan=2, padx=self.app.x_pad, pady=self.app.y_pad)

        print("Hello, world!")
        print(video_obj.title)
