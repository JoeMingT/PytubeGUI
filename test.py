from datetime import timedelta
import time
import threading
import customtkinter as ctk

def format_duration(duration):
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


def start_task(frame):
    thread = threading.Thread(target=background_task, daemon=True, args=())
    thread.start()
    frame.destroy()


def background_task():
    for i in range(10):
        print(f"Progress: {i+1}/10")
        time.sleep(1)
    print("Process Completed")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry(f"600x400")
    
    test_frame = ctk.CTkFrame(app)
    test_frame.pack()

    execute_task_btn = ctk.CTkButton(test_frame, command=lambda: start_task(test_frame))
    execute_task_btn.pack()

    app.mainloop()

