import customtkinter as ctk
import logging
import config as conf
from widgets.ConfigMenu import ConfigMenu
from widgets.MainMenu import MainMenu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize all global variables + configure settings
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme(conf._THEME_FILE_LOCATION)

        self.title("PyTubeGUI")
        self.x_pad = conf._DEFAULT_PAD_X
        self.y_pad = conf._DEFAULT_PAD_Y
        
        self.app_width = conf._SCREEN_WIDTH // 2
        self.app_height = conf._SCREEN_HEIGHT // 2
        self.app_x_pos = conf._SCREEN_WIDTH // 2 - self.app_width // 2
        self.app_y_pos = conf._SCREEN_HEIGHT // 2 - self.app_height // 2

        self.h1 = conf._H1_FONT
        self.h2 = conf._H2_FONT
        self.h3 = conf._H3_FONT
        self.p = conf._P_FONT
        
        self.geometry(f"{self.app_width}x{self.app_height}+{self.app_x_pos}+{self.app_y_pos}")

        self.generate_main_menu()

    def generate_main_menu(self):
        self.menu = MainMenu(self)
        self.menu.pack(padx=20, pady=20, anchor="center")
    
    def generate_config_menu(self, submitted_info):
        self.menu = ConfigMenu(self, submitted_info)
        self.menu.pack(padx=20, pady=20, anchor="center")

    def update_widget_attributes(self, widget, attributes):
        if widget.winfo_exists():
            widget.configure(**attributes)

