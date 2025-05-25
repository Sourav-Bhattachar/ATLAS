import tkinter as tk
from RUN import rotating_lines
from PIL import Image, ImageTk
import multiprocessing
import json
import os
root = tk.Tk()
root.title("ATLAS")
image = Image.open(r"ATLAS_UI_VIDEO_AUDIO\icon.ico")
icon = ImageTk.PhotoImage(image)
root.iconphoto(True, icon)
config_path = os.path.expanduser('~/.atlas_window_config.json')
saved_geometry = None
try:
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            saved_geometry = data.get('geometry')
except Exception as e:
    print(f"Error loading geometry: {e}")
if saved_geometry:
    root.geometry(saved_geometry)
else:
    window_width = 1250
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    cm_to_pixels = lambda cm: int(cm * (150 / 2.54))
    y_offset = cm_to_pixels(1.6)
    y_position = screen_height - window_height - y_offset
    x_position = (screen_width - window_width) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="black")
container = tk.Frame(root, width=1250, height=750, bg="black")
container.pack(expand=True, fill="both")

def play():
    print('Process is running')
    rotating_lines.play_rotating_lines(root, container)
    root.mainloop()
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=play)
        p1.start()
        p1.join()
        print("system stop")
