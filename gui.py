import time
from tktooltip import ToolTip
from PIL import Image
import tkinter as tk
import customtkinter as ctk
import config as conf

default_padding_x = conf._DEFAULT_PAD_X
default_padding_y = conf._DEFAULT_PAD_Y

def test(app, widget):
    time.sleep(1)
    widget.destroy() 
    generate_config_menu(app)

def generate_main_menu(app):
    # Frame
    main_menu_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_menu_frame.pack(padx=20, pady=20, anchor="center")

    # Title
    heading_label = ctk.CTkLabel(main_menu_frame, text="PytubeGUI", font=conf._H1_FONT)
    heading_label.grid(column=0, row=0, columnspan=2, padx=default_padding_x, pady=default_padding_y)

    # YouTube Link Input Field
    url_label = ctk.CTkLabel(main_menu_frame, text="YouTube URL:", font=conf._H3_FONT)
    url_label.grid(column=0, row=1, padx=default_padding_x, pady=default_padding_y, sticky="W")
    url_input = ctk.CTkEntry(main_menu_frame, width=conf._SCREEN_WIDTH//4, font=conf._P_FONT)
    url_input.grid(column=1, row=1, padx=default_padding_x, pady=default_padding_y, sticky="EW")

    # Convertion Type Frame
    convert_type_frame = ctk.CTkFrame(main_menu_frame)
    convert_type_frame.grid(column=0, row=2, columnspan=2, sticky="W", padx=default_padding_x, pady=default_padding_y)
    
    # 2 Two Types to Convert Into
    convert_type_var = tk.IntVar(value=1)
    video_radio_btn = ctk.CTkRadioButton(convert_type_frame, text="Video", variable=convert_type_var, value=1, font=conf._P_FONT)
    video_radio_btn.grid(column=0, row=0, pady=default_padding_y, padx=default_padding_x)
    audio_radio_btn = ctk.CTkRadioButton(convert_type_frame, text="Audio", variable=convert_type_var, value=2, font=conf._P_FONT)
    audio_radio_btn.grid(column=1, row=0, pady=default_padding_y, padx=default_padding_x)
 
    """
    # PO Token field
    po_token_var = tk.StringVar(value="off")
    po_token_checkbox = ctk.CTkCheckBox(main_menu_frame, text="Use PO Token?", variable=po_token_var, onvalue="on", offvalue="off")
    po_token_checkbox.grid(column=0, row=3, padx=default_padding_x, pady=default_padding_y, sticky="W")
    # Initializing Image Object
    tooltip_icon = ctk.CTkImage(light_image=Image.open("./assets/images/info_box_black.png"), dark_image=Image.open("./assets/images/info_box_white.png"))
    po_token_tooltip = ctk.CTkLabel(main_menu_frame, image=tooltip_icon, text="")           # Display image using Label
    # Set tooltip for more info regarding PO Token
    ToolTip(po_token_tooltip, msg="PO Token is used in deailing with Bots. If you failed converting a video multiple times, you may try switching on this option to avoid getting blocked.", delay=0.3, follow=True)
    po_token_tooltip.grid(column=1, row=3, pady=default_padding_y, sticky="W")

    # Use OAuth Field
    oauth_var = tk.StringVar(value="off")
    oauth_checkbox = ctk.CTkCheckBox(main_menu_frame, text="Use OAuth?", variable=oauth_var, onvalue="on", offvalue="off")
    oauth_checkbox.grid(column=0, row=4, padx=default_padding_x, pady=default_padding_y, sticky="W")
    oauth_tooltip = ctk.CTkLabel(main_menu_frame, image=tooltip_icon, text="")           # Display image using Label
    # Set tooltip for more info regarding PO Token
    ToolTip(oauth_tooltip, msg="OAuth means logging into your YouTube account to access the video. This allows you to bypass age-restricted content or potentially fixing being blocked. However, you risk getting your account BANNED! Be careful turning this on!", delay=0.3, follow=True)
    oauth_tooltip.grid(column=1, row=4, pady=default_padding_y, sticky="W")
    """
    # Submit Details for Conversion Button
    convert_button = ctk.CTkButton(main_menu_frame, text="Convert!", font=conf._H3_FONT, command=lambda: test(app, main_menu_frame))
    convert_button.grid(column=0, row=5, padx=default_padding_x, pady=default_padding_y)


def generate_config_menu(app):
    config_menu_frame = ctk.CTkFrame(app, fg_color="transparent")
    config_menu_frame.pack(padx=20, pady=20)
    
    heading_label = ctk.CTkLabel(config_menu_frame, text="Testing", font=conf._H1_FONT)
    heading_label.grid(column=0, row=0, columnspan=2, padx=default_padding_x, pady=default_padding_y)
