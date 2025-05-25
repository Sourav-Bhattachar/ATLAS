import cv2
import tkinter as tk
from PIL import Image, ImageTk
from RUN import face2
from playsound import playsound
from RUN import FaceAuthSuccessful
VIDEO_1 = r'ATLAS_UI_VIDEO_AUDIO\start_video.mp4'
VIDEO_WIDTH, VIDEO_HEIGHT = 1200, 800
TEXT_ANIMATION = "Ready For Face Authentication..."
TEXT_SPEED = 70

def play_rotating_lines(root, container):
    """Play rotating lines video, animate text, then clear canvas and switch to face2 video."""
    music_dir  = r'ATLAS_UI_VIDEO_AUDIO\start_sound.mp3'
    playsound(music_dir)
    cap = cv2.VideoCapture(VIDEO_1)
    video_label = tk.Label(container, bg="black")
    video_label.place(relx=0.5, rely=0.53, anchor="center")
    text_label = tk.Label(container, text="", font=("Arial", 24, "bold"), fg="white", bg="black")
    text_label.place(relx=0.5, rely=0.8, anchor="center")
    stop_video = False

    def update_frame():
        """Update video frames safely."""
        if stop_video:
            cap.release()
            return
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            if video_label.winfo_exists():
                video_label.imgtk = imgtk
                video_label.config(image=imgtk)
                root.after(15, update_frame)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def clear_canvas():
        """Stop video loop, clear UI, and switch to face2.py."""
        nonlocal stop_video
        stop_video = True
        for widget in container.winfo_children():
            widget.destroy()
        root.after(10, lambda: face2.play_face2(root, container))
    update_frame()
    root.after(5000, clear_canvas)
