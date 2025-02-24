import customtkinter as ctk

class DownloadWindow(ctk.CTkToplevel):
    def __init__(self, app, configuration_info, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.app = app
        self.geometry("400x300")

        self.title_label = ctk.CTkLabel(self, text="Downloads", font=self.app.h1)
        self.title_label.grid(column=0, row=0, columnspan=2)
        

