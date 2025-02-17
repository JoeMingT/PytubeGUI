import time
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
    main_menu_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_menu_frame.pack(padx=20, pady=20)

    heading_label = ctk.CTkLabel(main_menu_frame, text="PytubeGUI", font=conf._H1_FONT)
    heading_label.grid(column=0, row=0, columnspan=2, padx=default_padding_x, pady=default_padding_y)

    url_label = ctk.CTkLabel(main_menu_frame, text="YouTube URL:", font=conf._H3_FONT)
    url_label.grid(column=0, row=1, padx=default_padding_x, pady=default_padding_y, sticky="W")
    url_input = ctk.CTkEntry(main_menu_frame, width=conf._SCREEN_WIDTH//4, font=conf._P_FONT)
    url_input.grid(column=1, row=1, padx=default_padding_x, pady=default_padding_y, sticky="EW")

    convert_type_frame = ctk.CTkFrame(main_menu_frame)
    convert_type_frame.grid(column=0, row=2, columnspan=2, sticky="W", ipadx=default_padding_x)

    convert_type_var = tk.IntVar(value=1)
    video_radio_btn = ctk.CTkRadioButton(convert_type_frame, text="Video", variable=convert_type_var, value=1)
    video_radio_btn.grid(column=0, row=0, pady=default_padding_y)
    audio_radio_btn = ctk.CTkRadioButton(convert_type_frame, text="Audio", variable=convert_type_var, value=2)
    audio_radio_btn.grid(column=1, row=0, pady=default_padding_y)
    
    convert_button = ctk.CTkButton(main_menu_frame, text="Convert!", command=lambda: test(app, main_menu_frame))
    convert_button.grid(column=0, row=3, padx=default_padding_x, pady=default_padding_y)

def generate_config_menu(app):
    config_menu_frame = ctk.CTkFrame(app, fg_color="transparent")
    config_menu_frame.pack(padx=20, pady=20)
    
    heading_label = ctk.CTkLabel(config_menu_frame, text="Testing", font=conf._H1_FONT)
    heading_label.grid(column=0, row=0, columnspan=2, padx=default_padding_x, pady=default_padding_y)
