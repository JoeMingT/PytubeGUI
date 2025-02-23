from http.client import RemoteDisconnected
import customtkinter as ctk
import threading
import tkinter as tk
import pytubefix as pt
from tktooltip import ToolTip
from PIL import Image
import pytubefix.exceptions as ptexc

class MainMenu(ctk.CTkFrame):
    """The Main Menu of the application (Home Screen)

    Attributes: 
        app: widgets.App.App
        loading_status: str | None 
        yt: YouTube | None
        error_msg: str | None
        exception: Exception | None
        tooltip_icon: customtkinter.CTkImage
    """

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, fg_color="transparent", *args, **kwargs)
        self.app = app
        # Initialize global variables (to pass between widgets)
        self.loading_status = None
        self.yt = None
        self.error_msg = None
        self.exception = None
        # Initializing Image Object
        self.tooltip_icon = ctk.CTkImage(light_image=Image.open("./assets/images/info_box_black.png"), dark_image=Image.open("./assets/images/info_box_white.png"), size=(15,15))
        
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
        
        # Console label
        self.console_label = ctk.CTkLabel(self, text="Console", font=self.app.p)
        self.console_label.grid(column=0, row=6, sticky="W")
        # Console field
        self.console_field = ctk.CTkTextbox(self, wrap="word", width=self.app.app_width//2, height=125, state="disabled")
        self.console_field.grid(column=0, row=7, columnspan=2, sticky="EW")

        # Add some keybindings for smoother input
        self.convert_button.bind("<Return>", lambda event: self.convert_button.invoke())
        self.url_input.bind("<Return>", lambda event: self.convert_button.invoke())

        # When startup, focus on the url input field (faster input)
        self.url_input.focus()

    def log_to_main_menu_console(self, message):
        """Log a message to the GUI's console

        Args:
            message (string): Message to be logged to the user
        """
        if message[:-2] != "\n":
            message += "\n"
        self.console_field.configure(state="normal")
        self.console_field.insert(tk.END, message)
        self.console_field.see(tk.END)
        self.console_field.configure(state="disabled")

    def navigate_to_config_menu(self):
        """Destroys the main menu and navigate to the configuration menu for the next step"""
        self.pack_forget()  # Hide the window only, call it when Configuration menu is destroyed
        self.app.generate_config_menu({
            "yt": self.yt,
            "type": "video" if self.convert_type_var.get() == 1 else "audio",
            "main_menu": self
        })

    def fetch_youtube_data(self):
        """Fetch the data of the provided YouTube URL and handles any exception that occurrs"""
        self.loading_status = "loading"
        try:
            self.yt = pt.YouTube(self.url_input.get())
            ## Access the object so it loads fully
            self.yt.title
            self.yt.length
            self.loading_status = "completed"
        except ptexc.RegexMatchError as e:
            self.error_msg = "Please fill in a valid URL!"
            self.exception = e
            self.loading_status = "error"
        except ptexc.VideoUnavailable as e:
            self.error_msg = "Video Unavailable!"
            self.exception = e
            self.loading_status = "error"
        except RemoteDisconnected as e:
            self.error_msg = "Network Unstable and Disconnected! Try again!"
            self.exception = e
            self.loading_status = "error"
        except Exception as e:
            self.error_msg = "Unknown"
            self.exception = e
            self.loading_status = "error"


    def run_loading_animation(self):
        """Animate the 'Loading...' text with dots. Once loading complete, do the corresponding action (if it succeeded or failed)"""
        # When the status is loading (meaning pytube is still fetching data from the url provided)
        # Run the loading animation
        if self.loading_status == "loading":
            current_text = self.convert_button.cget("text")
            if "..." in current_text:
                new_text = "Loading"
            else:
                new_text = current_text + "."
            self.convert_button.configure(text=new_text)
            self.app.after_id = self.app.after(500, lambda: self.run_loading_animation())  # Repeat animation every 500ms 
        # When it's completed or error, call respective functions
        # To break recursive
        elif self.loading_status == "completed":
            self.convert_button.configure(text="Convert!", state="enabled")
            self.navigate_to_config_menu()
        elif self.loading_status == "error":
            self.convert_button.configure(text="Convert!", state="enabled")
            if self.error_msg == "Unknown":
                self.log_to_main_menu_console(f"Error! {type(self.exception).__name__}:\n{self.error_msg}")
            else:
                self.log_to_main_menu_console(f"Error! {type(self.exception).__name__}:\n{self.error_msg}")


    def start_fetching_data(self):
        """Fetches the data from the provided URL in another thread (so the GUI doesn't freeze and can multitask)"""
        # Disable the button so there won't be multiple requests
        self.convert_button.configure(text="Loading", state="disabled")
        # Start the thread
        pytube_thread = threading.Thread(
            target=self.fetch_youtube_data, 
            args=(),
            daemon=True
        )
        pytube_thread.start()
        # Start the loading animation at the same time
        self.run_loading_animation()
