import threading
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from RUN import handshake
from RUN.tts_manager import tts_controller

def speak(text):
    tts_controller.speak(text)

def stop_speaking():
    tts_controller.stop()

VIDEO_3 = r'ATLAS_UI_VIDEO_AUDIO\FaceAuthSuccessful.mp4'
VIDEO_WIDTH, VIDEO_HEIGHT = 280, 280
TEXT_ANIMATION = "Face Authentication Successful..."
TEXT_SPEED = 80
VIDEO_REPEAT_LIMIT = 5
video_animation_speed = 22

def play_success(root, container):
    threading.Thread(
        target=tts_controller.speak,
        args=("Face Authentication Successful",),
        daemon=True
    ).start()
    """Play face authentication success video and animate text."""
    container.destroy()
    cap = cv2.VideoCapture(VIDEO_3)
    success_container = tk.Frame(root, width=1200, height=700, bg="black")
    success_container.pack(expand=True, fill="both")
    success_label = tk.Label(success_container, bg="black")
    success_label.place(relx=0.5, rely=0.4, anchor="center", width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
    text_label = tk.Label(success_container, text="", font=("Arial", 24, "bold"), fg="white", bg="black")
    text_label.place(relx=0.5, rely=0.8, anchor="center")
    stop_animation = False
    stop_video = False
    video_play_count = 0

    def update_frame():
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
            success_label.imgtk = imgtk
            success_label.config(image=imgtk)
            root.after(video_animation_speed, update_frame)
        else:
            cap.release()
            video_play_count += 1

            if video_play_count < VIDEO_REPEAT_LIMIT:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                update_frame()
            else:
                root.after(10, lambda: handshake.play_handshake(root, success_container))

    def animate_text():
        """Loop text animation until it's fully displayed."""
        index = 0

        def show_text(*args):
            nonlocal index

            if index < len(TEXT_ANIMATION) and not stop_animation:

                if text_label.winfo_exists():
                    text_label.config(text=TEXT_ANIMATION[:index + 1])
                    index += 1
                    root.after(TEXT_SPEED, show_text)
                else:
                    print("Text label does not exist anymore. Stopping animation.")
            else:
                print("Text animation completed.")
        show_text()
    animate_text()
    update_frame()
