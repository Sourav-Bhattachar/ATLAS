import cv2
import tkinter as tk
from PIL import Image, ImageTk
from RUN.main_atlas import MainATLAS
import threading
from RUN.tts_manager import tts_controller

def speak(text):
    tts_controller.speak(text)

def stop_speaking():
    tts_controller.stop()
VIDEO_4 = r'ATLAS_UI_VIDEO_AUDIO\handshake.mp4'
MUSIC_DIR = r'ATLAS_UI_VIDEO_AUDIO\start_sound.mp3'
VIDEO_WIDTH, VIDEO_HEIGHT = 400, 400
WELCOME_TEXT = "Hello!! Welcome Sir, How Can I Help You?"
TEXT_SPEED = 90
VIDEO_REPEAT_LIMIT = 5
VIDEO_ANIMATION_SPEED = 20

def play_handshake(root, container):
    print(WELCOME_TEXT)
    threading.Thread(
        target=tts_controller.speak,
        args=(WELCOME_TEXT,),
        daemon=True
    ).start()
    """Play handshake video and display welcome message."""
    container.destroy()
    cap = cv2.VideoCapture(VIDEO_4)
    final_container = tk.Frame(root, width=1200, height=700, bg="black")
    final_container.pack(expand=True, fill="both")
    final_label = tk.Label(final_container, bg="black")
    final_label.place(relx=0.5, rely=0.4, anchor="center", width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
    final_text_label = tk.Label(final_container, text="", font=("Arial", 24, "bold"), fg="white", bg="black")
    final_text_label.place(relx=0.5, rely=0.8, anchor="center")
    stop_video = False
    video_play_count = 0

    def update_frame():
        """Update video frames and loop until the repeat limit is reached."""
        nonlocal video_play_count
        if stop_video:
            cap.release()
            return
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            final_label.imgtk = imgtk
            final_label.config(image=imgtk)
            root.after(VIDEO_ANIMATION_SPEED, update_frame)
        else:
            cap.release()
            video_play_count += 1
            if video_play_count < VIDEO_REPEAT_LIMIT:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                update_frame()
            else:
                root.after(300, lambda: [final_container.destroy(), MainATLAS(root)])

    def animate_text():
        """Animate welcome text letter by letter."""
        index = 0

        def show_text():
            nonlocal index
            if index <= len(WELCOME_TEXT):
                final_text_label.config(text=WELCOME_TEXT[:index+1])
                index += 1
                root.after(TEXT_SPEED, show_text)
        show_text()
    threading.Thread(target=animate_text, daemon=True).start()
    update_frame()
