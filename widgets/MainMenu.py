import customtkinter as ctk
import traceback
import threading
import tkinter as tk
import pytubefix as pt
from tktooltip import ToolTip
from PIL import Image
import pytubefix.exceptions as ptexc
from widgets.ConfigMenu import ConfigMenu

class MainMenu(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app, fg_color="transparent")
        self.app = app
        self.loading_status = None
        self.yt = None
        self.error_msg = None
        self.exception = None
        # Initializing Image Object
        self.tooltip_icon = ctk.CTkImage(light_image=Image.open("./assets/images/info_box_black.png"), dark_image=Image.open("./assets/images/info_box_white.png"))
        
        # Title
        self.heading_label = ctk.CTkLabel(self, text="PytubeGUI", font=self.app.h1)
        self.heading_label.grid(column=0, row=0, columnspan=2, padx=self.app.x_pad, pady=self.app.y_pad)

        # YouTube Link Input Field
        self.url_label = ctk.CTkLabel(self, text="YouTube URL:", font=self.app.h3)
        self.url_label.grid(column=0, row=1, padx=self.app.x_pad, pady=self.app.y_pad, sticky="W")
        self.url_input = ctk.CTkEntry(self, width=self.app.app_width//2, font=self.app.p)
        self.url_input.grid(column=1, row=1, padx=self.app.x_pad, pady=self.app.y_pad, sticky="EW")

        # Convertion Type Frame
        self.convert_type_frame = ctk.CTkFrame(self)
        self.convert_type_frame.grid(column=0, row=2, columnspan=2, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        
        # 2 Two Types to Convert Into
        self.convert_type_var = tk.IntVar(value=1)
        self.video_radio_btn = ctk.CTkRadioButton(self.convert_type_frame, text="Video", variable=self.convert_type_var, value=1, font=self.app.p)
        self.video_radio_btn.grid(column=0, row=0, pady=self.app.y_pad, padx=self.app.x_pad)
        self.audio_radio_btn = ctk.CTkRadioButton(self.convert_type_frame, text="Audio", variable=self.convert_type_var, value=2, font=self.app.p)
        self.audio_radio_btn.grid(column=1, row=0, pady=self.app.y_pad, padx=self.app.x_pad)
    
        # PO Token field
        self.po_token_var = tk.StringVar(value="off")
        self.po_token_checkbox = ctk.CTkCheckBox(self, text="Use PO Token?", variable=self.po_token_var, onvalue="on", offvalue="off")
        self.po_token_checkbox.grid(column=0, row=3, padx=self.app.x_pad, pady=self.app.y_pad, sticky="W")
        self.po_token_tooltip = ctk.CTkLabel(self, image=self.tooltip_icon, text="")           # Display image using Label
        # Set tooltip for more info regarding PO Token
        ToolTip(self.po_token_tooltip, msg="PO Token is used in detecting Bots. If you failed converting a video multiple times, you may try switching on this option to avoid getting blocked. (WIP)", delay=0.3, follow=True)
        self.po_token_tooltip.grid(column=1, row=3, pady=self.app.y_pad, sticky="W")

        # Use OAuth Field
        self.oauth_var = tk.StringVar(value="off")
        self.oauth_checkbox = ctk.CTkCheckBox(self, text="Use OAuth?", variable=self.oauth_var, onvalue="on", offvalue="off")
        self.oauth_checkbox.grid(column=0, row=4, padx=self.app.x_pad, pady=self.app.y_pad, sticky="W")
        self.oauth_tooltip = ctk.CTkLabel(self, image=self.tooltip_icon, text="")           # Display image using Label
        # Set tooltip for more info regarding PO Token
        ToolTip(self.oauth_tooltip, msg="OAuth means logging into your YouTube account to access the video. This allows you to bypass age-restricted content or potentially fixing being blocked. However, you risk getting your account BANNED! Be careful turning this on! (WIP)", delay=0.3, follow=True)
        self.oauth_tooltip.grid(column=1, row=4, pady=self.app.y_pad, sticky="W")

        # Submit Details for Conversion Button
        self.convert_button = ctk.CTkButton(self, text="Convert!", font=self.app.h3, 
                                                command=lambda: self.start_fetching_data()
                                            )
        self.convert_button.grid(column=0, row=5, padx=self.app.x_pad, pady=20)

        self.console_label = ctk.CTkLabel(self, text="Console", font=self.app.p)
        self.console_label.grid(column=0, row=6, sticky="W")
        
        self.console_field = ctk.CTkTextbox(self, wrap="word", width=self.app.app_width//2, height=125, state="disabled")
        self.console_field.grid(column=0, row=7, columnspan=2, sticky="EW")

    def log_to_main_menu_console(self, message):
        if message[:-2] != "\n":
            message += "\n"
        self.console_field.configure(state="normal")
        self.console_field.insert(tk.END, message)
        self.console_field.see(tk.END)
        self.console_field.configure(state="disabled")

    def navigate_to_config_menu(self):
        self.app.generate_config_menu(self.yt)
        self.destroy()

    def fetch_youtube_data(self):
        self.loading_status = "loading"
        try:
            print(self.url_input.get())
            self.yt = pt.YouTube(self.url_input.get())
            self.loading_status = "completed"
        except ptexc.RegexMatchError as e:
            self.error_msg = "Please fill in a valid URL!"
            self.exception = e
            self.loading_status = "error"
        except ptexc.VideoUnavailable as e:
            self.error_msg = "Video Unavailable!"
            self.exception = e
            self.loading_status = "error"
        except Exception as e:
            self.error_msg = "Unknown"
            self.exception = e
            self.loading_status = "error"


    def run_loading_animation(self):
        """Animate the 'Loading...' text with dots."""
        if self.loading_status == "loading":
            current_text = self.convert_button.cget("text")
            if "..." in current_text:
                new_text = "Loading"
            else:
                new_text = current_text + "."
            self.app.update_widget_attributes(self.convert_button, { "text": new_text })
            self.app.after_id = self.app.after(500, lambda: self.run_loading_animation())  # Repeat animation every 500ms 
        elif self.loading_status == "completed":
            self.navigate_to_config_menu()
        elif self.loading_status == "error":
            self.app.update_widget_attributes(self.convert_button, { "text": "Convert!", "state": "enabled" })
            if self.error_msg == "Unknown":
                self.log_to_main_menu_console(f"Error! {type(self.exception).__name__}:\n{traceback.format_exception(self.exception)}")
            else:
                self.log_to_main_menu_console(f"Error! {type(self.exception).__name__}:\n{self.error_msg}")

    def start_fetching_data(self):
        self.app.update_widget_attributes(self.convert_button, { "text": "Loading", "state": "disabled" })
        pytube_thread = threading.Thread(
            target=self.fetch_youtube_data, 
            args=(),
            daemon=True
        )
        pytube_thread.start()
        self.run_loading_animation()
