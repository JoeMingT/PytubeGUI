import customtkinter as ctk
from datetime import timedelta
import requests
from io import BytesIO
from PIL import Image

class ConfigMenu(ctk.CTkFrame):
    def __init__(self, app, submitted_info):
        super().__init__(app, fg_color="transparent")
        self.app = app
        self.yt = submitted_info["yt"]
        self.convert_type = submitted_info["type"]
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
        self.video_details_frame.grid(column=0, row=0, columnspan=20, row_span=3, sticky="NSEW", ipadx=20, ipady=10)
        self.video_details_frame.grid_columnconfigure(0, weight=1)  # allow columns to expand
        self.video_details_frame.grid_columnconfigure(1, weight=1)  # allow columns to expand
        self.video_details_frame.grid_rowconfigure(0, weight=1)    # allow rows to expand
        self.video_details_frame.grid_rowconfigure(1, weight=1)    # allow rows to expand
        self.video_details_frame.grid_rowconfigure(2, weight=1)    # allow rows to expand

        # Display Thumbnail (in one column)
        self.video_thumbnail = ctk.CTkLabel(self.video_details_frame, image=self.thumbnail_image, text="", anchor="center")
        self.video_thumbnail.grid(column=0, row=0, rowspan=3, sticky="NSEW", padx=self.app.x_pad, pady=self.app.y_pad)

        # Display video name, duration, and download size (dynamically change based on resolution selected) (In another column)
        self.video_title = ctk.CTkLabel(self.video_details_frame, text=f"Video: {self.truncate_text(self.yt.title)}", anchor="w", font=self.app.p, width=self.app.app_width//4)
        self.video_title.grid(column=1, row=0, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.video_duration = ctk.CTkLabel(self.video_details_frame, text=f"Duration: {self.format_duration(self.yt.length)}", anchor="w", font=self.app.p)
        self.video_duration.grid(column=1, row=1, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)
        self.video_size =  ctk.CTkLabel(self.video_details_frame, text=f"Size: {32}kb", anchor="w", font=self.app.p)
        self.video_size.grid(column=1, row=2, sticky="W", padx=self.app.x_pad, pady=self.app.y_pad)

        # Configuration Fields (Scrollable)
        # Put more important configuration on the top
        # Put less important, optional configuration on the bottom
        # Make it useless for now, make it so that it's possible to download video first
        """
        Fields that should have, from most important to less important
        === Must Haves (Do this first) ===
        1. Resolution
        2. Duration
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
        self.options_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.options_frame.grid(column=0, row=1, sticky="NSEW", padx=self.app.x_pad, pady=self.app.y_pad)

        self.resolution_dropdown = ctk.CTkComboBox(self.options_frame)


    def truncate_text(self, text):
        """Truncate a text that's too long

        Args:
            text (str): The text that should be truncated

        Returns:
            The truncated text or the original text if it doesn't exceed a limit
        """
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

    def filter_and_get_resolution(self):
        if self.convert_type == "audio":
            pass
        elif self.convert_type == "video":
            pass
