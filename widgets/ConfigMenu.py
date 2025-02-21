import customtkinter as ctk
import pytubefix as pt
import tkinter as tk
from tkinter import filedialog
import os
from datetime import timedelta
from customtkinter.windows.widgets import image
import requests
from io import BytesIO
from PIL import Image

class ConfigMenu(ctk.CTkFrame):
    def __init__(self, app, submitted_info):
        super().__init__(app, fg_color="transparent")
        self.app = app
        self.yt = submitted_info["yt"]
        self.convert_type = submitted_info["type"]
        self.streams = self.yt.streams.filter(only_audio=True) if self.convert_type == "audio" else self.yt.streams.filter(only_video=True)
        self.resolution_options = []
        self.format_and_get_resolution()

        # Initialize default image
        self.thumbnail_image_light = Image.open("./assets/images/image_not_found_black.png")
        self.thumbnail_image_dark = Image.open("./assets/images/image_not_found_white.png")
        # Try fetching thumbnail
        try:
            response = requests.get(self.yt.thumbnail_url)
            response.raise_for_status()
            self.thumbnail_image_light = Image.open(BytesIO(response.content))
            self.thumbnail_image_dark = self.thumbnail_image_light
        except:
            pass
        self.thumbnail_image = ctk.CTkImage(light_image=self.thumbnail_image_light, dark_image=self.thumbnail_image_dark, size=(self.app.app_width//5, self.app.app_height//5))
        
        # Show Video Details Section
        self.video_details_frame = ctk.CTkFrame(self)
        self.video_details_frame.grid(column=0, row=0, columnspan=20, rowspan=3, sticky="NSEW", ipadx=20, ipady=10)
        self.video_details_frame.grid_columnconfigure(0, weight=1)  # allow columns to expand
        self.video_details_frame.grid_columnconfigure(1, weight=1)  # allow columns to expand
        self.video_details_frame.grid_rowconfigure(0, weight=1)    # allow rows to expand
        self.video_details_frame.grid_rowconfigure(1, weight=1)    # allow rows to expand
        self.video_details_frame.grid_rowconfigure(2, weight=1)    # allow rows to expand

        # Display Thumbnail (in one column)
        self.video_thumbnail = ctk.CTkLabel(self.video_details_frame, image=self.thumbnail_image, text="", anchor="center")
        self.video_thumbnail.grid(column=0, row=0, rowspan=3, sticky="NSEW", padx=self.app.x_pad, pady=self.app.y_pad)

        # Variable for dynamic file size
        self.video_size_var = tk.StringVar(value="")
        # Set default video size
        self.update_file_size(self.resolution_options[0])
        # Display video name, duration, and download size (dynamically change based on resolution selected) (In another column)
        self.video_title = ctk.CTkLabel(self.video_details_frame, text=f"Video: {self.truncate_text(self.yt.title)}", anchor="w", font=self.app.p, width=self.app.app_width//4)
        self.video_title.grid(column=1, row=0, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.video_duration = ctk.CTkLabel(self.video_details_frame, text=f"Duration: {self.format_duration(self.yt.length)}", anchor="w", font=self.app.p)
        self.video_duration.grid(column=1, row=1, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.video_size = ctk.CTkLabel(self.video_details_frame, textvariable=self.video_size_var, anchor="w", font=self.app.p)
        self.video_size.grid(column=1, row=2, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

        # Configuration Fields (Scrollable)
        # Put more important configuration on the top
        # Put less important, optional configuration on the bottom
        # Make it useless for now, make it so that it's possible to download video first
        """
        Fields that should have, from most important to less important
        === Must Haves (Do this first) ===
        1. Resolution
        2. Duration (Removed. Not possible with pytubefix, may revisit for a workaround)
        3. Title / File Name
        4. Download Folder / Location
        === Other Settings ===
        X. Download Captions / Lyrics (If available)
        X. Download Thumbnail (If available) / Or upload own Thumbnail (Album Art, Cover Art)
        X. Add Indexing (Playlist things, so maybe need to check)
        === Metadata ===
        X. Year
        X. Tags / Genre
        X. Track Number
        X. Album (Playlist things, so maybe need to check)
        """
        # Frame to contain all the configuration option
        self.options_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=int(self.app.app_width/1.5))
        self.options_frame.grid(column=0, row=4, columnspan=2, sticky="NSEW", padx=self.app.x_pad, pady=self.app.y_pad)

        # Resolution Field
        self.resolution_var = tk.StringVar(value=self.resolution_options[0])
        self.resolution_label = ctk.CTkLabel(self.options_frame, text="Resolution:", font=self.app.h3)
        self.resolution_label.grid(column=0, row=0, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.resolution_dropdown = ctk.CTkComboBox(self.options_frame, 
                                                   font=self.app.p, 
                                                   values=self.resolution_options, 
                                                   variable=self.resolution_var, 
                                                   command=self.update_file_size)
        self.resolution_dropdown.grid(column=1, row=0, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        
        # Title / File Name Field
        self.title_var = tk.StringVar(value=f"{self.yt.title}")
        self.title_label = ctk.CTkLabel(self.options_frame, text="Video Name:", font=self.app.h3)
        self.title_label.grid(column=0, row=1, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.title_field = ctk.CTkEntry(self.options_frame, textvariable=self.title_var, width=self.app.app_width//2, font=self.app.p)
        self.title_field.grid(column=1, row=1, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

        # Download Folder / Location Field
        self.download_label = ctk.CTkLabel(self.options_frame, text="Download Folder:", font=self.app.h3)
        self.download_label.grid(column=0, row=2, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        
        # Add a frame to add a button beside the entry without eating up another column
        self.download_frame = ctk.CTkFrame(self.options_frame)
        self.download_frame.grid(column=1, row=2, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

        # The Entry Field
        self.download_loc_var = tk.StringVar(value=f"{self.get_download_folder_location()}")
        self.download_entry = ctk.CTkEntry(self.download_frame, textvariable=self.download_loc_var, width=self.app.app_width//3, font=self.app.p)
        self.download_entry.grid(column=0, row=0, sticky="E")
        # A Folder Icon
        self.folder_icon = ctk.CTkImage(light_image=Image.open("./assets/images/folder_black.png"), 
                                        dark_image=Image.open("./assets/images/folder_white.png"), 
                                        size=(20, 20))
        # A Button Icon when clicked will prompt user to select the download destination
        self.choose_loc_btn = ctk.CTkButton(self.download_frame, image=self.folder_icon, text="", width=25, command=lambda: self.query_download_destination())
        self.choose_loc_btn.grid(column=1, row=0, sticky="W", padx=self.app.x_pad//2)

        # Download Button
        self.download_button = ctk.CTkButton(self.options_frame, text="Download!", font=self.app.h3)
        self.download_button.grid(column=0, row=3, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

        self.back_button = ctk.CTkButton(self.options_frame, 
                                         text="Back", 
                                         font=self.app.h3,
                                         fg_color=("#E5E5E5", "#444B50"),
                                         hover_color=("#D3D3D3", "#62686D"),
                                         border_color=("#A98BC6", "#8A6BBE"),
                                         text_color=("#5A4B81", "#DCE4EE"),
                                         text_color_disabled=("gray60", "gray50"),
                                         command=lambda: self.return_to_main_menu()
                                         )
        self.back_button.grid(column=1, row=3, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

# secondary_button_styles = {
#     "fg_color": ["#E5E5E5", "#444B50"],  # Soft gray in light mode, darker gray in dark mode
#     "hover_color": ["#D3D3D3", "#62686D"],  # Slightly darker gray when hovered
#     "border_color": ["#A98BC6", "#8A6BBE"],  # Lavender border for subtle contrast
#     "text_color": ["#5A4B81", "#DCE4EE"],  # Dark lavender text in light mode, off-white in dark mode
#     "text_color_disabled": ["gray60", "gray50"]  # Softer grays for disabled state
# }

    def truncate_text(self, text):
        """Truncate a text that's too long

        Args:
            text (str): The text that should be truncated

        Returns:
            The truncated text or the original text if it doesn't exceed a limit """
        if len(text) > 30:
            truncated_text = text[:30]
            truncated_text = truncated_text[:-3] + "..."
            return truncated_text
        else:
            return text


    def format_duration(self, duration):
        """Format the duration of the video (which is in seconds) into a proper format

        Args:
            duration (int): Duration of the video in seconds
        """
        time_obj = timedelta(seconds=duration)
        
        days = time_obj.days
        hours, remainder = divmod(time_obj.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
        elif hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    def format_and_get_resolution(self):
        for i in range(len(self.streams)):
            stream = self.streams[i]
            if self.convert_type == "audio":
                self.resolution_options.append(f"{i+1}- {stream.bitrate} Hz, {stream.audio_codec}")
            else:
                self.resolution_options.append(f"{i+1}- {stream.resolution}, {stream.video_codec}")

    def get_download_folder_location(self):
        """Get the default download location of the user's computer machine

        Returns:
            The path to the default Download path
        """
        # Windows
        if os.name == "nt":  
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        # Linux or Mac
        else:  
            return os.path.join(os.environ["HOME"], "Downloads")


    def query_download_destination(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.download_loc_var.set(selected_dir)


    def update_file_size(self, current_choice):
        option_index = int(current_choice.split("-")[0])-1
        self.video_size_var.set(f"Size: {self.streams[option_index].filesize_mb:.2f}MB")


    def start_downloading(self):
        # May pass it into a new menu so that the user can keep track of it
        pass


    def return_to_main_menu(self):
        """Return to the main menu (In case of misinput or miscopied)"""
        self.destroy()
        self.app.generate_main_menu()
