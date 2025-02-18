import logging
import threading
import time
import pytubefix as pt
import gui

loading_status = "idle"
youtube_object = None

def getting_youtube_object(youtube_url=""):
    update_loading_status("loading")
    global youtube_object
    try:
        youtube_object = pt.YouTube(youtube_url)
        update_loading_status("completed")
    except Exception as e:
        update_loading_status("failed")
        logging.error(f"Error Encountered: {e}")

def update_loading_status(status):
    global loading_status
    loading_status = status


def fetch_youtube_data(app, main_menu_frame, button_widget, main_menu_info, completed_callback, failed_callback):
    # logging.info("Clicked on Convert")
    # print(main_menu_info["url"])
    # pytube_thread = threading.Thread(target=getting_youtube_object, args=f"{main_menu_info['url']}", daemon=True)
    # pytube_thread.start()
    # logging.info("Start Loading Animation")
    #
    # loading_animation(app, main_menu_frame, button_widget)
    # for i in range(5):
    #     print(i)
    #     time.sleep(1)
    global youtube_object
    try:
        youtube_object = pt.YouTube(url=main_menu_info["url"])
        completed_callback(app, main_menu_frame, youtube_object)
    except Exception as e:
        failed_callback(button_widget)
        

def loading_animation(app, main_menu_frame, button_widget):
    """Animate the 'Loading...' text with dots."""
    if loading_status == "loading":
        current_text = button_widget.cget("text")
        if "..." in current_text:
            new_text = "Loading"
        else:
            new_text = current_text + "."
        update_widget_attributes(button_widget, { "text": new_text })
        app.after(500, lambda: loading_animation(app, main_menu_frame, button_widget))  # Repeat animation every 500ms 
    elif loading_status == "completed": 
        main_menu_frame.destroy()
        gui.generate_config_menu(app, youtube_object)
    elif loading_status == "failed":
        update_widget_attributes(button_widget, { "text": "Convert!", "state": "enabled" })


def update_widget_attributes(widget, attributes):
    if widget.winfo_exists():
        widget.configure(**attributes)


def kill_tkinter_widget(widget):
    if widget.winfo_exists():
        widget.destroy()

