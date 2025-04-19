import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
# import FaceAuthSuccessful
from RUN import FaceAuthSuccessful
from RUN.face_recog import authenticate_face
from RUN.tts_manager import tts_controller




VIDEO_2 = r'ATLAS_UI_VIDEO_AUDIO\face2.mp4'
VIDEO_WIDTH, VIDEO_HEIGHT = 400, 400
TEXT_ANIMATION = "Ready For Face Authentication..."
TEXT_SPEED = 70


def speak(text):
    tts_controller.speak(text)

def stop_speaking():
    tts_controller.stop() 




def play_face2(root, container):
    """Play face authentication animation and authenticate face."""
    print(TEXT_ANIMATION)
    threading.Thread(
        target=tts_controller.speak, 
        args=(TEXT_ANIMATION,),
        daemon=True
    ).start()

    cap = cv2.VideoCapture(VIDEO_2)
    
    video_label = tk.Label(container, bg="black")
    video_label.place(relx=0.5, rely=0.4, anchor="center")

    # Text label
    text_label = tk.Label(container, text="", font=("Arial", 24, "bold"), fg="white", bg="black")
    text_label.place(relx=0.5, rely=0.8, anchor="center")

    stop_animation = threading.Event()  # Event to stop looping animations

    def update_frame():
        """Loop video frames until face recognition is successful."""
        if stop_animation.is_set():
            cap.release()
            if video_label.winfo_exists():
                video_label.config(image="")
            return

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video from beginning
        else:
            frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

        root.after(15, update_frame)

    def animate_text():
        """Loop text animation until face recognition is successful."""
        index = 0

        def show_text():
            nonlocal index
            if stop_animation.is_set():
                return

            if index <= len(TEXT_ANIMATION):
                text_label.config(text=TEXT_ANIMATION[:index])
                index += 1
                root.after(TEXT_SPEED, show_text)
            else:
                root.after(1000, restart_text)


        def restart_text():
            """Restart text animation."""
            nonlocal index
            if stop_animation.is_set():
                return
            index = 0
            show_text()

        show_text()

    def on_success(*args):
        """Stop animations, clear UI, and transition to the next UI."""
        stop_animation.set()  # Stop animations
        cap.release()

        if video_label.winfo_exists():
            video_label.config(image="")
        if text_label.winfo_exists():
            text_label.config(text="")

        
        FaceAuthSuccessful.play_success(root, container)  # Trigger next UI animation

    update_frame()
    animate_text()

    # Run face authentication in a separate thread
    threading.Thread(target=lambda: authenticate_face(root, container, on_success), daemon=True).start()












