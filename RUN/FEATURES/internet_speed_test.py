import socket
import tkinter as tk
import math
import threading
import speedtest
import time
from speedtest import SpeedtestException

class InternetSpeedometer:
    def __init__(self, root,callback=None):
        self.root = root
        self.callback = callback
        self.root.title("Internet Speedometer")
        self.root.geometry("1000x500")
        self.root.resizable(False, False)

        if not self.is_internet_available():
            self.show_error_message("No internet connection!")
            return
        
        self.download_animating = False
        self.upload_animating = False
        self.max_speed = 100  # Mbps
        self.radius = 150
        self.stop_flag = False
        self.tasks_completed = 0

        self.download_center = (250, 250)
        self.upload_center = (750, 250)

        self.canvas = tk.Canvas(root, width=1000, height=500, bg='black')
        self.canvas.pack()

        # Draw both speedometers
        self.draw_speedometer(self.download_center, "Download")
        self.draw_speedometer(self.upload_center, "Upload")

        # Needles
        self.download_needle = self.canvas.create_line(0, 0, 0, 0, width=4, fill='red')
        self.upload_needle = self.canvas.create_line(0, 0, 0, 0, width=4, fill='red')

        self.set_needle(self.download_needle, self.download_center, 0)
        self.set_needle(self.upload_needle, self.upload_center, 0)

        # Speed labels
        self.download_label = tk.Label(root, text="↓ 0.00 Mbps", font=('Arial', 16), bg='black', fg='white')
        self.download_label.place(x=180, y=400)

        self.upload_label = tk.Label(root, text="↑ 0.00 Mbps", font=('Arial', 16), bg='black', fg='white')
        self.upload_label.place(x=690, y=400)

        self.start_btn = tk.Button(
            self.root, text="Start Test", command=self.start_test,
            font=('Arial', 14), bg='green', fg='white'
        )
        self.stop_btn = tk.Button(
            self.root, text="Stop Test", command=self.stop_test,
            font=('Arial', 14), bg='red', fg='white'
        )
        self.start_btn.place(relx=0.5, rely=0.8, anchor='center')
        self.stop_btn.place_forget() 

        self.start_test()

    def is_internet_available(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

    def draw_speedometer(self, center, label):
        for i in range(0, self.max_speed + 10, 10):
            angle = math.radians(180 * i / self.max_speed)
            x_outer = center[0] + self.radius * math.cos(angle)
            y_outer = center[1] - self.radius * math.sin(angle)
            x_inner = center[0] + (self.radius - 15) * math.cos(angle)  # Tick line inner point
            y_inner = center[1] - (self.radius - 15) * math.sin(angle)

            # Draw tick line
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill='white', width=2)

            # Calculate position for labels with smaller radius
            label_radius = self.radius - 60  # Reduced from 15 to 25 (smaller radius)
            x_label = center[0] + label_radius * math.cos(angle)
            y_label = center[1] - label_radius * math.sin(angle)

            # Adjust text anchor based on angle quadrant
            angle_deg = 180 * i / self.max_speed
            anchor = 'w' if angle_deg <= 90 else 'e'  # 'w' for left-align, 'e' for right-align
            
            # Add label
            self.canvas.create_text(
                x_label, y_label,
                text=str(i),
                fill='white',
                font=('Arial', 10),
                anchor=anchor  # Dynamic alignment
            )

        # Rest of the code (center circle, label) remains unchanged...
        self.canvas.create_oval(center[0]-10, center[1]-10, center[0]+10, center[1]+10, fill='red')
        self.canvas.create_text(center[0], center[1] + 100, text=label, fill='white', font=('Arial', 16))
        
    def set_needle(self, needle, center, speed):
        angle = 180 * min(speed, self.max_speed) / self.max_speed
        rad = math.radians(angle)
        x = center[0] + (self.radius - 70) * math.cos(rad)
        y = center[1] - (self.radius - 70) * math.sin(rad)
        self.canvas.coords(needle, center[0], center[1], x, y)

    def animate_needle(self, needle, center, target_speed, label_widget, prefix):
        current_speed = 0
        step = (target_speed - current_speed) / 50  # Smoother animation
        for _ in range(50):
            if self.stop_flag:
                break
            current_speed += step
            self.set_needle(needle, center, current_speed)
            label_widget.config(text=f"{prefix} {current_speed:.2f} Mbps")
            time.sleep(0.02)
        if not self.stop_flag:
            self.set_needle(needle, center, target_speed)
            label_widget.config(text=f"{prefix} {target_speed:.2f} Mbps")
            return True
        else:
            self.set_needle(needle, center, 0)
            label_widget.config(text=f"{prefix} 0.00 Mbps")
            return False

    def start_test(self):
        self.stop_flag = False
        self.tasks_completed = 0
        self.start_btn.place_forget()
        self.stop_btn.place(relx=0.5, rely=0.8, anchor='center')
        threading.Thread(target=self.run_speed_test, daemon=True).start()

    def run_speed_test(self):
        try:
            st = speedtest.Speedtest()
            st.get_servers()
        except SpeedtestException as e:
            self.handle_speedtest_error(str(e))
            return
        except Exception as e:
            self.handle_speedtest_error(f"Unexpected error: {str(e)}")
            return

        def download_task():
            try:
                # Start animation
                self.download_animating = True
                self.root.after(0, lambda: [
                    self.download_label.config(text="↓ ", fg='yellow'),
                    self.animate_typing(self.download_label, "↓", "Testing...")
                ])
                download = st.download() / 1_000_000
                if self.stop_flag:
                    return
                # Stop animation and update result
                self.download_animating = False
                completed = self.animate_needle(self.download_needle, self.download_center, download, 
                                            self.download_label, "↓")
                if completed:
                    self.root.after(0, self.on_task_completed)
                self.root.after(0, lambda: self.download_label.config(fg='lightgreen'))
            except Exception as e:
                self.download_animating = False
                self.handle_speedtest_error(f"Download error: {str(e)}")

        def upload_task():
            try:
                # Start animation
                self.upload_animating = True
                self.root.after(0, lambda: [
                    self.upload_label.config(text="↑ ", fg='yellow'),
                    self.animate_typing(self.upload_label, "↑", "Testing...")
                ])
                upload = st.upload() / 1_000_000
                if self.stop_flag:
                    return
                # Stop animation and update result
                self.upload_animating = False
                completed = self.animate_needle(self.upload_needle, self.upload_center, upload, 
                                            self.upload_label, "↑")
                if completed:
                    self.root.after(0, self.on_task_completed)
                self.root.after(0, lambda: self.upload_label.config(fg='lightgreen'))
            except Exception as e:
                self.upload_animating = False
                self.handle_speedtest_error(f"Upload error: {str(e)}")

        threading.Thread(target=download_task).start()
        threading.Thread(target=upload_task).start()

    def on_task_completed(self):
        self.tasks_completed += 1
        if self.tasks_completed == 2:
            download = float(self.download_label.cget("text").split()[1])
            upload = float(self.upload_label.cget("text").split()[1])
            
            # Execute callback if provided
            if self.callback:
                self.callback(download, upload)

            self.stop_btn.place_forget()
            self.start_btn.place(relx=0.5, rely=0.8, anchor='center')
            self.tasks_completed = 0
    
    def handle_speedtest_error(self, error_message):
        self.root.after(0, lambda: self.show_error_message(
            f"Speed test failed!\n{error_message}", 
            show_retry=True
        ))
        pass

    def show_error_message(self, message, show_retry=True):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self.root, width=1000, height=500, bg='black')
        self.canvas.pack()

        error_label = tk.Label(
            self.root, 
            text=message, 
            font=('Arial', 16), 
            fg='red', 
            bg='black',
            wraplength=800
        )
        error_label.place(relx=0.5, rely=0.5, anchor='center')

        if show_retry:
            retry_btn = tk.Button(
                self.root,
                text="Retry",
                command=self.retry_connection,
                font=('Arial', 14),
                bg='green',
                fg='white',
                activebackground='green',
                activeforeground='white',
                border=0
            )
            retry_btn.place(relx=0.5, rely=0.6, anchor='center')

    def retry_connection(self):
        # Destroy existing widgets and reinitialize
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def stop_test(self):
        self.stop_flag = True
        self.download_animating = False
        self.upload_animating = False
        self.stop_btn.place_forget()
        self.start_btn.place(relx=0.5, rely=0.8, anchor='center')
        self.set_needle(self.download_needle, self.download_center, 0)
        self.set_needle(self.upload_needle, self.upload_center, 0)
        self.download_label.config(text="↓ 0.00 Mbps", fg='white')
        self.upload_label.config(text="↑ 0.00 Mbps", fg='white')

    def animate_typing(self, label_widget, prefix, full_text, step=0, direction=1):
        # Stop condition: Check animation flags or prefix mismatch
        if not label_widget.winfo_exists():  # Check if the widget still exists
            return
        current_text = label_widget.cget("text")
        expected_prefix = f"{prefix} "
        
        # Check if animation should continue
        if (prefix == "↓" and not self.download_animating) or \
        (prefix == "↑" and not self.upload_animating) or \
        not current_text.startswith(expected_prefix):
            return
        
        current_display = current_text[len(expected_prefix):]
        
        if direction == 1:  # Typing phase
            if len(current_display) < len(full_text):
                new_text = f"{prefix} {full_text[:len(current_display)+1]}"
                label_widget.config(text=new_text)
                self.root.after(100, lambda: self.animate_typing(label_widget, prefix, full_text, step+1, 1))
            else:  # Switch to erasing
                self.root.after(500, lambda: self.animate_typing(label_widget, prefix, full_text, 0, -1))
        else:  # Erasing phase
            if len(current_display) > 0:
                new_text = f"{prefix} {current_display[1:]}"
                label_widget.config(text=new_text)
                self.root.after(100, lambda: self.animate_typing(label_widget, prefix, full_text, step+1, -1))
            else:  # Restart typing
                self.root.after(500, lambda: self.animate_typing(label_widget, prefix, full_text, 0, 1))








# if __name__ == '__main__':
#     root = tk.Tk()
#     app = InternetSpeedometer(root)
#     root.mainloop()

    
