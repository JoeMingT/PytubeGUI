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
        
        # Set light or dark mode, based on user's system'
        ctk.set_appearance_mode("System")  
        # Get custom theme of lavender (Obtained from https://github.com/a13xe/CTkThemesPack)
        ctk.set_default_color_theme(conf._THEME_FILE_LOCATION)
        
        # Set title
        self.title("PyTubeGUI")

        # Global constants from config.py
        # Passed down into the child component to be used easily
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
        
        # Set the size of the window
        self.geometry(f"{self.app_width}x{self.app_height}+{self.app_x_pos}+{self.app_y_pos}")
        
        # Initialize the main menu
        self.generate_main_menu()

    def generate_main_menu(self):
        """Generate the main menu GUI, which is the home page of the GUI application"""
        self.menu = MainMenu(self)
        self.menu.pack(padx=20, pady=20, anchor="center")
    
    def generate_config_menu(self, submitted_info):
        """Generate the configuration menu which displays the details of the video of the provided YouTube URL and a form to allow modification to the output.

        Args:
            submitted_info (dict()): The information submitted from the main menu, in a dictionary form. 
                                    Consists of "yt" and "type" keys, which contains the pytubefix YouTube object and the type of output that the user wanted
        """
        self.menu = ConfigMenu(self, submitted_info)
        self.menu.pack(padx=20, pady=20, anchor="center")

    def update_widget_attributes(self, widget, attributes):
        if widget.winfo_exists():
            widget.configure(**attributes)

