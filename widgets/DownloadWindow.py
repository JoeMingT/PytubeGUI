import customtkinter as ctk

class DownloadWindow(ctk.CTkToplevel):
    def __init__(self, app, configuration_info, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.app = app
        self.geometry("400x300")



