import logging
import pytubefix as pt
import customtkinter as ctk
import config as conf
import gui

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("./themes/lavender.json")

    app = ctk.CTk()

    x_pad = conf._DEFAULT_PAD_X
    y_pad = conf._DEFAULT_PAD_Y
    app_width = conf._SCREEN_WIDTH // 2
    app_height = conf._SCREEN_HEIGHT // 2
    app_x_pos = conf._SCREEN_WIDTH // 2 - app_width // 2
    app_y_pos = conf._SCREEN_HEIGHT // 2 - app_height // 2
    app.geometry(f"{app_width}x{app_height}+{app_x_pos}+{app_y_pos}")
    app.title("PytubeGUI")

    gui.generate_main_menu(app)

    app.mainloop()
