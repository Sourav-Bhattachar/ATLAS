from tkinter import ttk
from playsound import playsound
from PIL import Image, ImageTk
import ctypes
import json
import os
import tkinter as tk
import math
import random
import keyboard
import psutil
import sys
import pyttsx3
import speech_recognition as sr 
import threading  
import struct
import time
import pvporcupine
import pyaudio
import win32gui
import pyautogui
import google.generativeai as genai
import cv2
import colorsys
import screen_brightness_control as sbc
from RUN.commands import CommandHandler



music_dir = r'ATLAS_UI_VIDEO_AUDIO\start_sound.mp3'
MODEL_PATH = r'ATLAS_UI_VIDEO_AUDIO\atlas_en_windows_v3_0_0\atlas_en_windows_v3_0_0.ppn'
ACCESS_KEY = "KBA7OP80xfcHP4Eb4AcewbIifBNvGjunXnYBjRDt2a9qfqP/mhQ2ZQ=="

# Constants
WIDTH = 1650
HEIGHT = 980
DOT_COUNT = 700
RADIUS = 110
FOCAL_LENGTH = 5000
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
SW_MINIMIZE = 6
SW_RESTORE = 9
BASE_ANGLE = 1.5  
ANIMATION_INTERVAL = 20  # ~50 FPS 
MAX_DOTS = 10
NEW_DOT_SPANNING = 2 # (per frame) 

# send Btn ui ===>
center_x, center_y = 40, 40
btn_width, btn_height = 40, 40
corner_radius = 20
num_layers = 10
spacing = 1
glow_animation = None
glow_layers = []
frame = 0

# mke btn ui
canvas_width = 50
canvas_height = 60
mike_btn_border_width = 10
position_x,position_y  = 25,30

# chat history ui
CHAT_HISTORY_WIDTH = 500
SLIDE_SPEED = 100


# brightness ui
brightness_panel_speed = 100
brightness_panel_height = 400
brightness_panel_width = 200



class MainATLAS:
    
    THEMES = [
        {  # defaultTheme
            'name': 'Default Theme',
            'bg': 'black',
            'user_bg': '#0000ff',
            'bot_bg': '#002040',
            'highlightbackground': 'blue',
            'highlightcolor' : 'cyan',
            'timestamp': '#d1d1d1'
        },
        {  # dark red Theme
            'name': 'Dark Red Theme',
            'bg': 'black',
            'user_bg': '#420000',
            'bot_bg': '#002040',
            'highlightbackground': 'red',
            'highlightcolor' : 'magenta',
            'timestamp': '#d1d1d1'
        },
        {  # Dark Blue Theme
            'name': 'Dark Blue Theme',
            'bg': '#000a1a',
            'user_bg': '#003366',
            'bot_bg': '#1a0033',
            'highlightbackground': '#0099ff',
            'highlightcolor' : 'blue',
            'timestamp': '#a0a0a0'
        },
        {  # Cyberpunk Theme
            'name': 'Cyberpunk Theme',
            'bg': '#1a0a33',
            'user_bg': '#ff0099',
            'bot_bg': '#9900ff',
            'highlightbackground': '#00ffcc',
            'highlightcolor' : 'cyan',
            'timestamp': '#cccccc'
        },
        {  # Earth Tones
            'name': 'Earth Tones Theme',
            'bg': '#2c241b',
            'user_bg': '#4e3629',
            'bot_bg': '#3d4e36',
            'highlightbackground': '#c5a880',
            'highlightcolor' : '#bb7409',
            'timestamp': '#b0b0b0'
        },
        {  # Ocean Depths
            'name': 'Ocean Depths Theme',
            'bg': '#001f3f',
            'user_bg': '#0074D9',
            'bot_bg': '#39CCCC',
            'highlightbackground': '#7FDBFF',
            'highlightcolor': '#B10DC9',
            'timestamp': '#DDDDDD'
        },
        {  # Sunset Vibes
            'name': 'Sunset Vibes Theme',
            'bg': '#2d1a36',
            'user_bg': '#FF851B',
            'bot_bg': '#FF4136',
            'highlightbackground': '#F012BE',
            'highlightcolor': '#B10DC9',
            'timestamp': '#FFDC00'
        },
        {  # Forest Green
            'name': 'Forest Green Theme',
            'bg': '#1a2f1a',
            'user_bg': '#2E8B57',
            'bot_bg': '#3CB371',
            'highlightbackground': '#228B22',
            'highlightcolor': '#006400',
            'timestamp': '#98FB98'
        },
        {  # Midnight Purple
            'name': 'Midnight Purple Theme',
            'bg': '#0a0a1a',
            'user_bg': '#4B0082',
            'bot_bg': '#800080',
            'highlightbackground': '#9400D3',
            'highlightcolor': '#8A2BE2',
            'timestamp': '#E6E6FA'
        },
        {  # Retro Neon
            'name': 'Retro Neon Theme',
            'bg': '#2a2a2a',
            'user_bg': '#FF00FF',
            'bot_bg': '#00FF00',
            'highlightbackground': '#FFD700',
            'highlightcolor': '#FF1493',
            'timestamp': '#00FFFF'
        },
        {  # Coffee Stain
            'name': 'Coffee Stain Theme',
            'bg': '#3e2723',
            'user_bg': '#6d4c41',
            'bot_bg': '#8d6e63',
            'highlightbackground': '#a1887f',
            'highlightcolor': '#795548',
            'timestamp': '#d7ccc8'
        },
        {  # Ice Kingdom
            'name': 'Ice Kingdom Theme',
            'bg': '#0a1a2a',
            'user_bg': '#4682B4',
            'bot_bg': '#87CEEB',
            'highlightbackground': '#00BFFF',
            'highlightcolor': '#1E90FF',
            'timestamp': '#F0F8FF'
        },
        {  # Galaxy
            'name': 'Galaxy Theme',
            'bg': '#0a0612',
            'user_bg': '#6a1b9a',
            'bot_bg': '#9c27b0',
            'highlightbackground': '#e040fb',
            'highlightcolor': '#7c4dff',
            'timestamp': '#d1c4e9'
        },
        {  # Cyber Green
            'name': 'Cyber Green Theme',
            'bg': '#000f08',
            'user_bg': '#00ff88',
            'bot_bg': '#00c853',
            'highlightbackground': '#76ff03',
            'highlightcolor': '#64dd17',
            'timestamp': '#b9f6ca'
        },
        {  # Vintage Paper
            'name': 'Vintage Paper Theme',
            'bg': '#f5e6d3',
            'user_bg': '#d4b996',
            'bot_bg': '#c2a582',
            'highlightbackground': '#a68a64',
            'highlightcolor': '#8b7355',
            'timestamp': '#6b4f3a'
        },
        {  # Coral Reef
            'name': 'Coral Reef Theme',
            'bg': '#2d112c',
            'user_bg': '#ff4040',
            'bot_bg': '#ff6b6b',
            'highlightbackground': '#ff1493',
            'highlightcolor': '#ff69b4',
            'timestamp': '#ffb6c1'
        },
        {  # Golden Age
            'name': 'Golden Age Theme',
            'bg': '#1a1818',
            'user_bg': '#ffd700',
            'bot_bg': '#daa520',
            'highlightbackground': '#b8860b',
            'highlightcolor': '#cd950c',
            'timestamp': '#fffacd'
        }
    ]

    class Dot:
        def __init__(self, x, y, z, moving=False, direction=1, is_incoming=False):
            self.x = x
            self.y = y
            self.z = z
            self.moving = moving
            self.direction = direction
            self.speed = 4 if is_incoming else (5 if moving else 0)
            self.is_incoming = is_incoming
            self.hue = random.random()
            self.size = random.randint(1,2) if is_incoming else random.randint(1,2)

        def rotate_y(self, angle):
            damping_factor = 0.95  # Closer to 1 means smoother damping
            angle *= damping_factor

            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)
            x = self.x * cos_theta - self.z * sin_theta
            z = self.x * sin_theta + self.z * cos_theta
            self.x, self.z = x, z

        def move(self):
            if self.moving:
                scale = self.speed * self.direction
                norm = math.sqrt(self.x**2 + self.y**2 + self.z**2)
                if norm == 0:
                    return
                self.x += (self.x / norm) * scale
                self.y += (self.y / norm) * scale
                self.z += (self.z / norm) * scale

        def project(self, current_width, current_height):
            factor = FOCAL_LENGTH / (FOCAL_LENGTH + self.z)
            x = self.x * factor + current_width  / 2
            y = self.y * factor + current_height / 3.5
            return (x, y)
        
    class ReverseToolTip:
        def __init__(self, editor, widget, text_or_func):
            self.editor = editor
            self.widget = widget
            self.text_or_func = text_or_func  # Can be a string or a callable
            self.tipwindow = None
            self.widget.bind("<Enter>", self.showtip)
            self.widget.bind("<Leave>", self.hidetip)

        def showtip(self, event=None):
            if self.tipwindow:
                return
            # Calculate position relative to the main window
            x = self.widget.winfo_rootx() - 100
            y = self.widget.winfo_rooty() + 40
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)  # Remove window decorations
            tw.wm_geometry(f"+{x}+{y}")
            
            # Get the text dynamically if a function is provided
            if callable(self.text_or_func):
                text = self.text_or_func()
            else:
                text = self.text_or_func
                
            self.ReverseToolTip_label = tk.Label(
                tw, text=text, bg='black', fg="#ffff00", 
                font=("Consolas", 11, "italic")
            )
            self.ReverseToolTip_label.pack()

        def hidetip(self, event=None):
            if self.tipwindow:
                self.tipwindow.destroy()
            self.tipwindow = None

    class ToolTip:
        def __init__(self, editor, widget, text_or_func):
            self.editor = editor
            self.widget = widget
            self.text_or_func = text_or_func  # Can be a string or a callable
            self.tipwindow = None
            self.widget.bind("<Enter>", self.showtip)
            self.widget.bind("<Leave>", self.hidetip)

        def showtip(self, event=None):
            if self.tipwindow:
                return
            # Calculate position relative to the main window
            x = self.widget.winfo_rootx() + 35
            y = self.widget.winfo_rooty() + 40
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)  # Remove window decorations
            tw.wm_geometry(f"+{x}+{y}")
            
            # Get the text dynamically if a function is provided
            if callable(self.text_or_func):
                text = self.text_or_func()
            else:
                text = self.text_or_func
                
            self.ReverseToolTip_label = tk.Label(
                tw, text=text, bg='black', fg="#ffff00", 
                font=("Consolas", 11, "italic")
            )
            self.ReverseToolTip_label.pack()

        def hidetip(self, event=None):
            if self.tipwindow:
                self.tipwindow.destroy()
            self.tipwindow = None

    def __init__(self, root):
        self.root = root
        self.root.title("ATLAS") 
        self.root.overrideredirect(True)
        self.root.configure(bg='black')


        self.maximized = False
        self.chat_file = r'RUN\FEATURES\chat_history.json'
        self.is_busy = False
        self.frame_count = 0
        self.last_frame_time = time.time()
        self.delta_time = 0.016
        self.color_hue = 0
        self.clear_after_id = None 
        self.is_animating = True  
        self.command_animating = False  
        self.command_angle = 0 
        self.video_label = None
        self.cap = None
        self.running = True
        self.video_running = False
        self.is_fullscreen_text = False
        self.current_chunk = 0
        self.text_chunks = []
        self.placeholder_active = True 
        self.fullscreen_text = None
        self.scrollbar = None
        self.hotword_active = True 
        self.hue = 0
        self.animating = False
        self.after_id = None
        self.chat_history_open = False
        self.chat_history = []
        self.current_theme_index = 0 
        self.brightness_panel_open = False
        self.brightness_highlight_thickness = 2

    
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(pady=(85, 0), expand=True, fill= tk.BOTH)
        self.canvas.bind("<Button-1>", self.unfocus_entry)

        self.user_command_label = tk.Label(
            self.canvas, 
            text="", 
            bg="black", 
            fg="white", 
            font=("Arial", 14)
        )
        self.user_command_label.place(relx=0.5, y=30, anchor="center")

        self.bot_response_label = tk.Label(
            self.canvas, 
            text="", 
            bg="black", 
            fg="white", 
            font=("Arial", 14)
        )
        self.bot_response_label.place(relx=0.5, y=80, anchor="center")
               
        self.load_images()
        self.create_custom_UI()
        self.setup_battery_ui()
        self.setup_window_properties()
        self.root.update_idletasks()
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.maximized = (self.window_width == self.screen_width and self.window_height == self.screen_height)
        self.dots = self.generate_dots()
        self.animate()
        self.update_battery()
        self.track_focused_windows() 
        self.start_hotword_detection()
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 174)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) 
        self.root.bind('<Configure>', self.on_configure)
        self.command_handler = CommandHandler(self)
        keyboard.add_hotkey('windows + left', self.snap_left)
        keyboard.add_hotkey('windows + right', self.snap_right)
        self.create_chat_history_panel()
        self.load_chat_history()

    def load_images(self):
        self.icon_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\icon.png')).resize((35, 35))
        self.resize_toggle_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\resize_toggle.png')).resize((18, 18))
        self.send_message_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\send_message.png')).resize((35, 35))
        self.mike_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\mike_image.png')).resize((35, 37))
        self.three_dot_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\chat_history.png')).resize((35, 35))
        self.delete_chat_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\trash_bin.png')).resize((27, 35))
        self.brightness_image = Image.open(self.resource_path(r'ATLAS_UI_VIDEO_AUDIO\brightness.png')).resize((35, 35))


        self.icon_icon = ImageTk.PhotoImage(self.icon_image)
        self.resize_toggle_icon = ImageTk.PhotoImage(self.resize_toggle_image)
        self.send_message_icon = ImageTk.PhotoImage(self.send_message_image)
        self.mike_icon = ImageTk.PhotoImage(self.mike_image)
        self.three_dot_icon = ImageTk.PhotoImage(self.three_dot_image)
        self.delete_chat_icon = ImageTk.PhotoImage(self.delete_chat_image)
        self.brightness_icon = ImageTk.PhotoImage(self.brightness_image)

    def input_gloing_box(self):

        # custom frames 10 - 1
        self.message_input_send_mike_frame = tk.Frame(self.canvas, bg="black", highlightthickness=0)
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        self.multicolor_frame = tk.Frame(self.message_input_send_mike_frame, bg="black", highlightthickness=0)
        self.multicolor_frame.pack(side=tk.LEFT, padx=1.3, pady=1.3)

        self.frame_10 = tk.Frame(self.multicolor_frame, bg="black", highlightthickness=0)
        self.frame_10.pack(padx=1.3, pady=1.3)
        
        self.frame_9 = tk.Frame(self.frame_10, bg="black", highlightthickness=0)
        self.frame_9.pack(padx=1.3, pady=1.3)
        
        self.frame_8 = tk.Frame(self.frame_9, bg="black", highlightthickness=0)
        self.frame_8.pack(padx=1.3, pady=1.3)

        self.frame_7 = tk.Frame(self.frame_8, bg="black", highlightthickness=0)
        self.frame_7.pack(padx=1.3, pady=1.3)

        self.frame_6 = tk.Frame(self.frame_7, bg="black", highlightthickness=0)
        self.frame_6.pack(padx=1.3, pady=1.3)

        self.frame_5 = tk.Frame(self.frame_6, bg="black", highlightthickness=0)
        self.frame_5.pack(padx=1.3, pady=1.3)

        self.frame_4 = tk.Frame(self.frame_5, bg="black", highlightthickness=0)
        self.frame_4.pack(padx=1.3, pady=1.3)

        self.frame_3 = tk.Frame(self.frame_4, bg="black", highlightthickness=0)
        self.frame_3.pack(padx=1.3, pady=1.3)

        self.frame_2 = tk.Frame(self.frame_3, bg="black", highlightthickness=0)
        self.frame_2.pack(padx=1.3, pady=1.3)

        self.frame_1 = tk.Frame(self.frame_2, bg="black", highlightthickness=0)
        self.frame_1.pack(padx=1.3, pady=1.3)

        self.inner_frame = tk.Frame(self.frame_1, bg="blue", highlightthickness=0)
        self.inner_frame.pack(padx=1.3, pady=1.3)

        # ..........---------==============--------.............#

    def speak(self, text, callback=None):
        text = str(text)
        print(f"ATLAS: {text}")
        self.is_busy = True
        try:
            if self.engine._inLoop:
                self.engine.endLoop()
                self.engine.stop()
                
            # Use existing engine instance
            self.root.after(0, lambda: self.stop_speaking_btn.place(relx=0.5, rely=0.5, anchor='center'))
            self.root.after(0, lambda: self.atlas_text_label.place(relx=0.5, rely=0.5, anchor='center'))
            self.engine.say(text)
            self.engine.startLoop(False)  # Start new loop without blocking
            self.engine.iterate()  # Process the speech queue
        except Exception as e:
            print(f"Speak error: {e}")

        finally:
            if callback:
                self.root.after(100, self.check_speech_completion, callback)
        return text
    
    def resource_path(self, relative_path):
        """ Get absolute path to resources for both dev and PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        # Handle nested icon paths
        if 'icons' in relative_path:
            full_path = os.path.join(base_path, relative_path.replace('\\', os.sep))
        else:
            full_path = os.path.join(base_path, relative_path)
            
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Resource not found: {full_path}")
        return full_path

    def on_close(self):
        self.running = False
        if hasattr(self, 'battery_update_id'):
            self.root.after_cancel(self.battery_update_id)
        self.engine.stop()  # Stop ongoing speech
        self.save_geometry()
        self.root.destroy()

    def save_geometry(self):
        """Save current window geometry to a config file"""
        config_path = os.path.expanduser('~/.atlas_window_config.json')
        try:
            geometry = self.root.geometry()
            with open(config_path, 'w') as f:
                json.dump({'geometry': geometry}, f)
        except Exception as e:
            print(f"Error saving window geometry: {e}")

    def load_geometry(self):
        """Load window geometry from config file if exists"""
        config_path = os.path.expanduser('~/.atlas_window_config.json')
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get('geometry')
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error loading window geometry: {e}")
            return None

    def setup_window_properties(self):
        saved_geometry = self.load_geometry()
        if saved_geometry:
            self.root.geometry(saved_geometry)
        else:
            self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        # Set window icon
        try:
            self.root.iconbitmap(r'ATLAS_UI_VIDEO_AUDIO\icon.ico')
        except Exception as e:
            print(f"Icon error: {e}")

        # Windows-specific taskbar setup
        if sys.platform == 'win32':
            self.setup_win32_window()

    def setup_win32_window(self):
        try:
            self.root.withdraw()  # Hide window temporarily
            self.root.update_idletasks()
            
            # Get window handle after it exists
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())

            # Force window to be treated as application window
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ex_style &= ~WS_EX_TOOLWINDOW
            ex_style |= WS_EX_APPWINDOW 
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)

            # Show window properly
            self.root.deiconify()
            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
            
            # Force window to front and activate
            ctypes.windll.user32.SetWindowPos(
                hwnd, 
                -1,  # HWND_TOPMOST (ensure window stays on top)
                0, 0, 0, 0,
                0x0001 | 0x0002 | 0x0020  # SWP_NOSIZE | SWP_NOMOVE | SWP_SHOWWINDOW
            )
            ctypes.windll.user32.SetForegroundWindow(hwnd)

        except Exception as e:
            print(f"Window setup error: {e}")

    def create_custom_UI(self):
        playsound(music_dir)
        self.input_gloing_box()
        self.title_bar = tk.Frame(self.root, bg="gray15", relief='flat', height=40)
        self.title_bar.place(x=0, y=0, relwidth=1)

        self.battery_bar = tk.Frame(self.root, bg="black", relief='flat', height=40)
        self.battery_bar.place(x=0, y=45, relwidth=1)

        self.atlas_title_label = tk.Label(self.title_bar, text="ATLAS", bg="gray15", fg="yellow", font=("Times New Roman", 14))

        self.atlas_text_label = tk.Label(self.battery_bar, text="ATLAS", bg="black", fg="cyan", font=("Bodoni MT Black", 18))

        # user_input_box
        self.user_input_box = tk.Entry(self.inner_frame, 
                                       bg="black", 
                                       fg="gray", 
                                       font=("Arial", 12, 'italic'), 
                                       insertbackground="white", 
                                       border=0, 
                                       relief="flat", 
                                       width=50, 
                                       highlightthickness=0)
        self.user_input_box.pack(padx=1, pady=(1,1), ipady=4, side=tk.LEFT, fill=tk.X)
        self.user_input_box.insert(0, '     Message...')

        self.send_message_btn_canvas = tk.Canvas(self.message_input_send_mike_frame, width=80, height=80, highlightthickness=0, bg='black')
        self.ReverseToolTip(self,self.send_message_btn_canvas, "Send\nMessage...")

        def hsv_to_hex(h, s, v):
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))

        def draw_rounded_rect(x1, y1, x2, y2, radius, **kwargs):
            points = [
                (x1+radius, y1),
                (x2-radius, y1),
                (x2, y1),
                (x2, y1+radius),
                (x2, y2-radius),
                (x2, y2),
                (x2-radius, y2),
                (x1+radius, y2),
                (x1, y2),
                (x1, y2-radius),
                (x1, y1+radius),
                (x1, y1),
            ]
            return self.send_message_btn_canvas.create_polygon(points, smooth=True, **kwargs)

        def create_multicolor_glow():
            global glow_layers, frame
            for layer in glow_layers:
                self.send_message_btn_canvas.delete(layer)
            glow_layers.clear()

            for i in range(num_layers):
                expand = i * spacing
                hue = ((frame - i * 5) % 360) / 360

                # Brighter outer layers by fading slower
                brightness = max(0, 1 - (i / num_layers) ** 1.8)  # exponential fade
                saturation = 1  # You can also try 0.9 for slight pastel effect

                color = hsv_to_hex(hue, saturation, brightness)

                rect = draw_rounded_rect(
                    center_x - btn_width // 2 - expand,
                    center_y - btn_height // 2 - expand,
                    center_x + btn_width // 2 + expand,
                    center_y + btn_height // 2 + expand,
                    corner_radius + expand // 3,
                    fill=color, outline=""
                )
                self.send_message_btn_canvas.tag_lower(rect)
                glow_layers.append(rect)

        def animate_glow():
            global glow_animation, frame
            create_multicolor_glow()
            frame += 1
            glow_animation = root.after(5, animate_glow)

        def stop_glow():
            global glow_animation, glow_layers
            if glow_animation:
                root.after_cancel(glow_animation)
                glow_animation = None
            for layer in glow_layers:
                self.send_message_btn_canvas .delete(layer)
            glow_layers.clear()

        main_button = draw_rounded_rect(
            center_x - btn_width//2,
            center_y - btn_height//2,
            center_x + btn_width//2,
            center_y + btn_height//2,
            corner_radius,
            fill='black', outline=""
        )

        self.send_message_btn = self.send_message_btn_canvas.create_image(center_x, center_y, image=self.send_message_icon)
        
        for tag in (main_button, self.send_message_btn):
            self.send_message_btn_canvas.tag_bind(tag, "<Enter>", lambda e: animate_glow())
            self.send_message_btn_canvas.tag_bind(tag, "<Leave>", lambda e: stop_glow())
            self.send_message_btn_canvas.tag_bind(tag, "<Button-1>", self.handle_text_input)

        self.mike_btn_canvas = tk.Canvas(self.message_input_send_mike_frame,width=canvas_width,border=0,highlightthickness=0, height=canvas_height, bg="black")
        self.mike_btn_canvas.pack(side=tk.LEFT, padx=5, pady=5)
        self.ReverseToolTip(self,self.mike_btn_canvas, "Microphone...")

        def animate_border(canvas, border_width, animation_speed, hue_offset_container):

            canvas.delete("border")

            width = canvas.winfo_width()
            height = canvas.winfo_height()
            radius = min(width, height) // 3
            total_steps = 40 * 4 + 10 * 4  # 40 per line * 4 + 10 per arc * 4
            index = 0
            hue_offset = hue_offset_container[0]
            
            index = draw_gradient_line(canvas, 0, height - radius, 0, radius, border_width, "vertical", hue_offset, index, total_steps)

            index = draw_gradient_line(canvas, radius, height, width - radius, height, border_width, "horizontal", hue_offset, index, total_steps)

            index = draw_gradient_line(canvas, width, height - radius, width, radius, border_width, "vertical", hue_offset, index, total_steps)

            index = draw_gradient_line(canvas, width - radius, 0, radius, 0, border_width, "horizontal", hue_offset, index, total_steps)

            index = draw_smooth_arc(canvas, 0, height - radius * 2, radius * 2, height, 180, 90, border_width, hue_offset, index, total_steps)

            index = draw_smooth_arc(canvas, width - radius * 2, height - radius * 2, width, height, 270, 90, border_width, hue_offset, index, total_steps)

            index = draw_smooth_arc(canvas, width - radius * 2, 0, width, radius * 2, 0, 90, border_width, hue_offset, index, total_steps)

            index = draw_smooth_arc(canvas, 0, 0, radius * 2, radius * 2, 90, 90, border_width, hue_offset, index, total_steps)

            hue_offset_container[0] += 0.06
            if hue_offset_container[0] > 1:
                hue_offset_container[0] = 0

            canvas.after(animation_speed, animate_border, canvas, border_width, animation_speed, hue_offset_container)
    
        def draw_gradient_line(canvas, x1, y1, x2, y2, border_width, direction, hue_offset, start_index, total_steps):
            steps = 50 # higher = smoother
            dx = (x2 - x1) / steps
            dy = (y2 - y1) / steps

            for i in range(steps):
                global_step = start_index + i
                hue = (hue_offset + global_step / total_steps) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
                color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))

                start_x = x1 + i * dx
                start_y = y1 + i * dy
                end_x = x1 + (i + 1) * dx
                end_y = y1 + (i + 1) * dy

                canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=border_width, tags="border", capstyle='round')

            return start_index + steps

        def draw_smooth_arc(canvas, x1, y1, x2, y2, start_angle, extent, border_width, hue_offset, start_index, total_steps):
            steps = 50 # higher = smoother
            angle_step = extent / steps
            radius = (x2 - x1) / 2
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            last_x, last_y = None, None
            for i in range(steps + 1):
                angle = math.radians(start_angle + i * angle_step)
                x = cx + radius * math.cos(angle)
                y = cy - radius * math.sin(angle)

                if last_x is not None:
                    global_step = start_index + i
                    hue = (hue_offset + global_step / total_steps) % 1.0
                    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
                    color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
                    canvas.create_line(last_x, last_y, x, y, fill=color, width=border_width, tags="border", capstyle='round')

                last_x, last_y = x, y

            return start_index + steps

        hue_offset_container = [0]
        animate_border(self.mike_btn_canvas, border_width=7, animation_speed=10, hue_offset_container=hue_offset_container)

        self.mike_btn = self.mike_btn_canvas.create_image(position_x, position_y, image=self.mike_icon)
        self.mike_btn_canvas.tag_bind(self.mike_btn,'<Button-1>', lambda e: self.take_command())

        self.user_input_box.bind("<FocusIn>", self.start_animation)
        self.user_input_box.bind("<FocusOut>", self.stop_animation)
        self.user_input_box.bind("<Return>", self.handle_text_input)
        self.user_input_box.bind("<KeyRelease>", self.handel_send_btn_visibility)

        # Dragging functionality
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        keyboard.add_hotkey('windows + j', lambda: self.take_command() if not self.is_busy else None)
        self.create_window_controls()

    def create_window_controls(self):
        # App icon
        self.icon_stop_speaking_btn = tk.Button(self.title_bar, image=self.icon_icon, bg="gray15", fg="white", font=("Arial", 14),command=self.stop_speaking, border=0, borderwidth=0, activebackground="gray25", relief="flat")
        self.icon_stop_speaking_btn.pack(side=tk.LEFT, padx=10)
        self.atlas_title_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_speaking_btn = tk.Button(
            self.title_bar,
            text="⏹️",
            command=self.stop_speaking,
            bg="red",
            fg="white",
            activebackground="red",
            border=0,
            borderwidth=0,
            relief="flat",
            font=("Arial", 10)
        )
        self.ReverseToolTip(self,self.stop_speaking_btn, "Stop Speaking")

        self.toggle_minimize_btn = tk.Button(
            self.title_bar,
            text='—',
            command=self.minimize,
            bg="gray15",
            fg="white",
            border=0,
            borderwidth=0,
            activebackground="gray25",
            relief="flat",
            font=("Arial", 10)
        )
        self.ReverseToolTip(self,self.toggle_minimize_btn, "Minimize")

        self.toggle_full_screen_btn = tk.Button(
            self.title_bar,
            text='□',
            command=self.toggle_maximize,
            bg="gray15",
            fg="white",
            border=0,
            borderwidth=0,
            activebackground="gray25",
            relief="flat",
            font=("Arial", 15)
        )
        self.ReverseToolTip(self,self.toggle_full_screen_btn, "Fullscreen")

        self.toggle_resize_btn = tk.Button(
            self.title_bar,
            image=self.resize_toggle_icon,
            command=self.toggle_maximize,
            bg="gray15",
            fg="white", 
            border=0,
            borderwidth=0,
            activebackground="gray25",
            relief="flat",
            font=("Arial", 12)
        )
        self.ReverseToolTip(self,self.toggle_resize_btn, "Resize")

        self.close_window_btn = tk.Button(
            self.title_bar,
            text='✕',
            command=self.on_close,
            bg="gray15",
            fg="white",
            activebackground="gray25",
            border=0,
            borderwidth=0,
            relief="flat",
            font=("Arial", 12)
        )
        self.ReverseToolTip(self,self.close_window_btn, "Close")

        self.close_window_btn.pack(side=tk.RIGHT, padx=(0,10))
        self.toggle_minimize_btn.pack(side=tk.RIGHT, padx=0)

        self.root.bind_all("<Button-1>", self.close_brightness_panel)

        self.update_window_controls()

    def update_window_controls(self):
        # Hide both buttons to avoid duplicates
        self.toggle_full_screen_btn.pack_forget()
        self.toggle_resize_btn.pack_forget()
        self.close_window_btn.pack_forget()
        self.toggle_minimize_btn.pack_forget()

        if self.maximized:
            self.close_window_btn.pack(side=tk.RIGHT, padx=(0,10))
            self.toggle_resize_btn.pack(side=tk.RIGHT, padx=(15, 15))
            self.toggle_minimize_btn.pack(side=tk.RIGHT, padx=0)

        else:
            self.toggle_full_screen_btn.pack_forget()
            self.toggle_resize_btn.pack_forget()
            self.close_window_btn.pack_forget()
            self.toggle_minimize_btn.pack_forget()

            self.close_window_btn.pack(side=tk.RIGHT, padx=(0,10))
            self.toggle_full_screen_btn.pack(side=tk.RIGHT, padx=(5, 5))
            self.toggle_minimize_btn.pack(side=tk.RIGHT, padx=0)

    def minimize(self):
        if sys.platform == 'win32':
            try:
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                ctypes.windll.user32.ShowWindow(hwnd, SW_MINIMIZE)
            except Exception as e:
                print(f"Minimize error: {e}")
        else:
            self.root.iconify()

    def toggle_maximize(self):
        self.maximized = not self.maximized
        if self.maximized:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
            self.battery_bar.place_forget()
            self.battery_bar.place(x=0, y=42, relwidth=1)
        else:
            self.root.geometry(f"{WIDTH}x{HEIGHT}")
            self.battery_bar.place_forget()
            self.battery_bar.place(x=0, y=42, relwidth=1)
        self.update_window_controls()

        if self.is_fullscreen_text:
            self.adjust_text_size()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.root.geometry(f"+{event.x_root - self.x}+{event.y_root - self.y}")

    def setup_battery_ui(self):

        self.history_btn = tk.Button(
            self.battery_bar,
            image= self.three_dot_icon,
            command=self.toggle_chat_history,
            bg="black",
            fg="white",
            font=("Arial", 14),
            highlightbackground='black',
            activebackground='black',
            highlightthickness=0,
            border=0
        )
        self.history_btn.pack(side=tk.LEFT, padx=30, pady=(6,0))
        self.ToolTip(self, self.history_btn, "Chat History")

        self.brightness_btn = tk.Button(
            self.battery_bar,
            image= self.brightness_icon,
            command=self.toggle_brightness_panel,
            bg="black",
            fg="white",
            font=("Arial", 14),
            highlightbackground='black',
            activebackground='black',
            highlightthickness=0,
            border=0
        )
        self.brightness_btn.pack(side=tk.LEFT, padx=10, pady=(6,0))
        self.ToolTip(self, self.brightness_btn, "Screen Brightness\nController")

        self.battery_canvas = tk.Canvas(self.battery_bar, width=120, height=30, bg="black", highlightthickness=0)
        self.battery_canvas.pack(side=tk.RIGHT, padx=5, pady=(2, 0))
        self.ReverseToolTip(self, self.battery_canvas, self.get_battery_tooltip_text)
        

        self.brightness_panel = tk.Canvas(
            self.root,
            bg="black",
            height=brightness_panel_height,
            width=brightness_panel_width,
            highlightthickness=2,
            highlightbackground="blue",
            highlightcolor="cyan"
        )

        line_x = 100
        self.brightness_line = self.brightness_panel.create_line(
            line_x, 50, line_x, 350, fill="blue", width=3
        )
        
        # Knob with shadow
        knob_radius = 10
        self.knob_shadow = self.brightness_panel.create_oval(
            line_x - knob_radius - 2, 200 - knob_radius - 2,
            line_x + knob_radius + 2, 200 + knob_radius + 2,
            fill="red", outline="", tags="shadow"
        )
        
        self.knob = self.brightness_panel.create_oval(
            line_x - knob_radius, 200 - knob_radius,
            line_x + knob_radius, 200 + knob_radius,
            fill="magenta", outline="", tags="knob"
        )
        
        # Brightness label
        self.brightness_label = tk.Label(
            self.brightness_panel,
            text="100%",
            bg="black",
            fg="white",
            font=("Times New Roman", 15)
        )
        self.brightness_label.place(relx=0.5, rely=0.05, anchor="center")
        
        # Event bindings
        self.brightness_panel.tag_bind("knob", "<B1-Motion>", self.on_brightness_drag)
        self.brightness_panel.tag_bind("knob", "<Enter>", lambda e: self.brightness_panel.itemconfig("knob", fill="#5cc6ff"))
        self.brightness_panel.tag_bind("knob", "<Leave>", lambda e: self.brightness_panel.itemconfig("knob", fill="magenta"))
        
        # Initialize brightness
        try:
            self.current_brightness = sbc.get_brightness(display=0)[0]
            self.set_knob_position()
        except Exception as e:
            print(f"Brightness error: {e}")
            self.current_brightness = 50

        self.battery_x = 30
        self.battery_y = 5
        self.battery_width = 60
        self.battery_height = 22
        self.tip_width = 5
        self.tip_height = 8
                
        self.colors = {
            'high': '#00FF00',
            'medium': '#FFFF00',
            'low': '#FF0000',
            'background': '#000000',
            'outline': '#FFFFFF'
        }
        
        self.battery_canvas.create_rectangle(
            self.battery_x + self.battery_width,
            self.battery_y + (self.battery_height - self.tip_height)//2,
            self.battery_x + self.battery_width + self.tip_width,
            self.battery_y + (self.battery_height - self.tip_height)//2 + self.tip_height,
            outline="white",
            fill="black"
        )

        self.battery_body = self.battery_canvas.create_rectangle(
        self.battery_x,
        self.battery_y,
        self.battery_x + self.battery_width,
        self.battery_y + self.battery_height,
        outline="white",
        fill="#787878"
    )

        self.text_white = self.battery_canvas.create_text(
        self.battery_x + self.battery_width//2,
        self.battery_y + self.battery_height//2,
        text='',
        font=('Arial',9, 'bold'),
        fill='black',
        anchor='center'
    )

        self.charge_level = self.battery_canvas.create_rectangle(
        self.battery_x + 2,
        self.battery_y + 2,
        self.battery_x + 2,
        self.battery_y + self.battery_height - 2,
        outline='',
        fill='#00FF00'
    )

        self.text_black = self.battery_canvas.create_text(
        self.battery_x + self.battery_width//2,
        self.battery_y + self.battery_height//2,
        text='',
        font=('Arial', 9, 'bold'),
        fill='black',
        anchor='center'
    )

        self.charging_indicator = self.battery_canvas.create_text(
        self.battery_x + self.battery_width + self.tip_width + 8,
        self.battery_y + self.battery_height//2,
        text='',
        font=('Arial', 10),
        fill='green'
    )

    def update_battery(self):
        if not self.running:  # Stop if the app is closed
            return
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            charging = battery.power_plugged

            fill_width = (self.battery_width - 4) * (percent / 100)
            self.battery_canvas.coords(
                self.charge_level,
                self.battery_x + 2,
                self.battery_y + 2,
                self.battery_x + 2 + fill_width,
                self.battery_y + self.battery_height - 2
            )

            # Update text content
            self.battery_canvas.itemconfig(self.text_black, text=f"{int(percent)}%")
            self.battery_canvas.itemconfig(self.text_white, text=f"{int(percent)}%")

            # Update charge color
            color = (
                self.colors['low'] if percent <= 20 else
                self.colors['medium'] if percent <= 50 else
                self.colors['high']
            )
            self.battery_canvas.itemconfig(self.charge_level, fill=color)
            self.battery_canvas.itemconfig(self.charging_indicator, text="⚡" if charging else "")

        self.battery_update_id = self.root.after(20, self.update_battery)

    def generate_dots(self):
        dots = []
        for _ in range(DOT_COUNT):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            x = RADIUS * math.sin(phi) * math.cos(theta)
            y = RADIUS * math.sin(phi) * math.sin(theta)
            z = RADIUS * math.cos(phi)
            dots.append(self.Dot(x, y, z))
        return dots

    def animate(self):
        if not self.is_animating:
            return 
        
        current_time = time.time()
        self.delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        self.canvas.delete("dot")
        rotation_speed = BASE_ANGLE * self.delta_time * 0.7

        r, g, b = colorsys.hsv_to_rgb(self.color_hue, 1.0, 1.0)
        hex_color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

        current_width = self.canvas.winfo_width()
        current_height = self.canvas.winfo_height()

        for dot in self.dots:
            dot.rotate_y(rotation_speed)
            dot.move()
            x, y = dot.project(current_width, current_height)
            if 0 <= x <= current_width and 0 <= y <= current_height:
                self.canvas.create_oval(x - dot.size, y - dot.size, 
                                  x + dot.size, y + dot.size, 
                                  fill=hex_color, outline="", tags="dot")

        self.update_dots()

        self.color_hue += 0.009  # controls how fast the color changes
        if self.color_hue > 1.0:
            self.color_hue = 0

        self.animation_id = self.root.after(ANIMATION_INTERVAL, self.animate)

    def update_dots(self):
        self.frame_count += 1
        self.dots = [dot for dot in self.dots if 
                 (math.sqrt(dot.x**2 + dot.y**2 + dot.z**2) < RADIUS * 2.5) and 
                 not (dot.is_incoming and math.sqrt(dot.x**2 + dot.y**2 + dot.z**2) <= RADIUS)]

        missing_dots = MAX_DOTS - len(self.dots)
        if missing_dots > 0:
            for _ in range(missing_dots):
                theta = random.uniform(0, 2 * math.pi)
                phi = random.uniform(0, math.pi)
                x = RADIUS * 6 * math.sin(phi) * math.cos(theta)
                y = RADIUS * 2.5 * math.sin(phi) * math.sin(theta)
                z = RADIUS * 4 * math.cos(phi)
                self.dots.append(self.Dot(x, y, z, moving=True, direction=-1, is_incoming=True))

        for _ in range(NEW_DOT_SPANNING):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            x = 2 * RADIUS * math.sin(phi) * math.cos(theta)
            y = 2 * RADIUS * math.sin(phi) * math.sin(theta)
            z = 2 * RADIUS * math.cos(phi)
            self.dots.append(self.Dot(x, y, z, moving=True, direction=-1, is_incoming=True))
        

        for dot in random.sample(self.dots, k=min(2, len(self.dots))):
            if not dot.moving and not dot.is_incoming:
                dot.moving = True
                dot.direction = 1

    def track_focused_windows(self):
        def _tracker():
            focused_windows = []
            while True:
                current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if current_window and (not focused_windows or current_window != focused_windows[-1]):
                    focused_windows.append(current_window)
                    if len(focused_windows) > 2:
                        focused_windows.pop(0)
                time.sleep(0.5)

        threading.Thread(target=_tracker, daemon=True).start()

    def clear_command_labels(self):
        self.user_command_label.config(text="")
        self.bot_response_label.config(text="")
        self.clear_after_id = None

    def start_hotword_detection(self):
        def _hotword_listener():
            porcupine = None
            paud = None
            audio_stream = None
            
            try:
                porcupine = pvporcupine.create(
                    access_key=ACCESS_KEY,
                    keyword_paths=[MODEL_PATH]
                )
                paud = pyaudio.PyAudio()
                audio_stream = paud.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=porcupine.sample_rate,
                    input=True,
                    frames_per_buffer=porcupine.frame_length
                )

                while True:
                    data = audio_stream.read(porcupine.frame_length)
                    data = struct.unpack_from("h" * porcupine.frame_length, data)
                    keyword_index = porcupine.process(data)

                    if keyword_index >= 0 and self.hotword_active:
                        self.hotword_active = False
                        current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                        if current_window != "ATLAS":
                            pyautogui.hotkey('win', '1')  # Switch to taskbar position 1
                        
                        # pyautogui.press('~') # Simulate keypress
                        print("Hotword detected!\n")  
                        self.take_command()  # Trigger voice command

            except Exception as e:
                print(f"Hotword error: {e}")
            finally:
                if porcupine:
                    porcupine.delete()
                if audio_stream:
                    audio_stream.close()
                if paud:
                    paud.terminate()

        # Start the listener in a background thread
        threading.Thread(target=_hotword_listener, daemon=True).start()

    def take_command(self):
        if self.is_busy:  # Prevent taking command if already busy
            return
        self.is_busy = True 
        self.hotword_active = False
        self.is_animating = False  # Stop sphere animation
        self.canvas.delete("dot")  # Clear existing dots
        self.command_animating = True  # Start command animation

        self.user_command_label.place_forget()
        self.bot_response_label.place_forget()
        self.message_input_send_mike_frame.place_forget()
        
        # Initialize video
        self.video_path = os.path.join("ATLAS_UI_VIDEO_AUDIO", "listening.mp4")  # Update path

        self.cap = cv2.VideoCapture(self.video_path)
        self.video_running = True
        
        # Create video label
        self.video_label = tk.Label(self.canvas, bg="black")
        self.video_label.place(relx=0.5, rely=0.3, anchor="center")
        
        self.listening_label = tk.Label(self.canvas,text='', bg="black", fg='white', font=("Arial", 20))
        self.listening_label.place(relx=0.5, rely=0.6, anchor="center")
        self.animate_listening_text(self.listening_label, "Listening...")
        
        # Start video playback
        self._update_video_frame()
        threading.Thread(target=self.listen_and_recognize, daemon=True).start()
        playsound(music_dir)

    def listen_and_recognize(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.energy_threshold = 2
                r.pause_threshold = 1
                audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print(text)
            self.root.after(0, self.update_command_display, text)
        except sr.WaitTimeoutError:
            self.root.after(0, self.update_command_display, "No speech detected")
        except sr.UnknownValueError:
            self.root.after(0, self.update_command_display, "Could not understand audio")
        except sr.RequestError as e:
            self.root.after(0, self.update_command_display, f"Error: {e}")
        except Exception as e:
            self.root.after(0, self.update_command_display, f"Mic error: {e}")

    def update_command_display(self, text):
        self.video_running = False
        if self.cap:
            self.cap.release()
        if self.video_label:
            self.video_label.place_forget()
            self.listening_label.place_forget()
        
        # Show labels again
        self.user_command_label.place(relx=0.5, y=30, anchor="center")
        self.bot_response_label.place(relx=0.5, y=80, anchor="center")
        self.user_command_label.config(text=f"User :  {text}", font=("Arial", 20))
        self.execute_command(text)

    def chat_bot(self, text):
        text = str(text)
        genai.configure(api_key='AIzaSyCgepCd72RunvdGLuD-258qaawcWeHBubg')
        model = genai.GenerativeModel("gemini-1.5-flash")
        if 'with in' in text or 'within' in text:
            response = model.generate_content(text)
            return response.text
        else:
            try:
                response = model.generate_content(text+' with in 10 words')
                return response.text
            except Exception as e:
                return f"Error: {str(e)}"
    
    def schedule_label_clear(self):
        if self.clear_after_id:
            self.root.after_cancel(self.clear_after_id)
        self.clear_after_id = self.root.after(0, self.restore_sphere_animation)

    def restore_sphere_animation(self):
        if self.is_fullscreen_text:
            self.clear_fullscreen_text()

        if hasattr(self, 'animation_id'):
            self.root.after_cancel(self.animation_id)

        self.command_animating = False
        self.is_animating = True
        self.hotword_active = True

        self.canvas.delete("command_anim")
        self.user_command_label.config(text="")
        self.bot_response_label.config(text="")
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER) 
        self.animate()

        if self.clear_after_id:
            self.root.after_cancel(self.clear_after_id)
            self.clear_after_id = None

    def _update_video_frame(self):
        if self.video_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:  # Video ended, reset to beginning
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            if ret:
                # Resize logic
                max_width = 400  # Set your desired maximum dimensions
                max_height = 300
                
                # Get original dimensions
                height, width = frame.shape[:2]
                
                # Calculate scaling factor while preserving aspect ratio
                scale = min(max_width/width, max_height/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                # Resize frame
                frame = cv2.resize(frame, (new_width, new_height))
                
                # Rest of the code remains the same
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=imgtk)
                self.video_label.image = imgtk
            self.root.after(30, self._update_video_frame)

    def create_fullscreen_text(self):
        if self.fullscreen_text:
            return
            
        # Hide other UI elements
        self.canvas.pack_forget()
        self.battery_canvas.place_forget()
        
        # Create fullscreen text container
        self.text_frame = tk.Frame(self.root, bg='black')
        self.text_frame.pack(fill='both', expand=True,pady=(85, 5), padx=(5, 0))
        
        # Add scrollbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar",
                gripcount=0,
                background="black",  # Scrollbar track color
                troughcolor="black",  # Background color
                bordercolor="black",
                arrowcolor="black",
                relief="flat",
                width=14
            )
        style.map("Vertical.TScrollbar",
                            background=[("active", "magenta"), ("!active", "cyan")],
                            arrowcolor=[("active", "black"), ("!active", "magenta")]
                        )
                        
        self.scrollbar = ttk.Scrollbar(self.text_frame,
                                        style="Vertical.TScrollbar"
                                        )
        self.scrollbar.pack(side='right', fill='y', padx=(0,3))
        
        # Create text widget
        self.fullscreen_text = tk.Text(
            self.text_frame,
            wrap='word',
            bg='black',
            fg='white',
            insertbackground='white',
            font=('Arial', 14),
            yscrollcommand=self.scrollbar.set,
            padx=10,
            pady=10,
        )
        self.fullscreen_text.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.fullscreen_text.yview)
        
        self.fullscreen_text.bind('<Key>', self._handle_key_events)
        self.fullscreen_text.bind('<Button-3>', self._show_context_menu)
        self.fullscreen_text.bind('<<Cut>>', lambda e: 'break')
        self.fullscreen_text.bind('<<Paste>>', lambda e: 'break')

        
        # Configure tags for formatting
        self.fullscreen_text.tag_configure('response', spacing3=10)
        self.is_fullscreen_text = True
        
        # Bind window resize events
        self.root.bind('<Configure>', self.adjust_text_size)

    def adjust_text_size(self, event=None):
        if self.is_fullscreen_text and self.fullscreen_text:
            # Calculate font size based on window height
            new_size = max(12, int(self.root.winfo_height() / 50))
            self.fullscreen_text.config(font=('Arial', new_size))

    def clear_fullscreen_text(self):
        if not self.is_fullscreen_text:
            return
            
        self.root.unbind('<Configure>')
        self.text_frame.pack_forget()
        self.text_frame.destroy()
        self.fullscreen_text = None
        self.scrollbar = None
        self.is_fullscreen_text = False
        
        # Restore original UI elements
        self.canvas.pack(pady=(85, 0), expand=True, fill=tk.BOTH)
        self.battery_canvas.place(x=20, y=HEIGHT - 130)
        self.user_command_label.place(relx=0.5, y=30, anchor="center")
        self.bot_response_label.place(relx=0.5, y=80, anchor="center")
        self.battery_canvas.pack(side=tk.RIGHT, padx=10, pady=(5, 0))
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def stop_speaking(self):
        if self.engine._inLoop:  # Check if engine is actually speaking
            self.engine.endLoop()  # Properly end the event loop
            self.engine.stop()  # Stop current speech only
        if hasattr(self, 'check_speech_id'):
            self.root.after_cancel(self.check_speech_id)
            del self.check_speech_id
        self.root.after(0, self.restore_sphere_animation)
        self.root.after(0, self.stop_speaking_btn.place_forget)
        self.root.after(0, self.atlas_text_label.place_forget)
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.is_busy = False

    def check_speech_completion(self, callback):
        if self.engine.isBusy():
            self.check_speech_id =self.root.after(100, self.check_speech_completion, callback)
        else:
            self.stop_speaking_btn.place_forget()
            self.atlas_text_label.place_forget()
            self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
            playsound(music_dir)
            self.is_busy = False
            callback()
            if hasattr(self, 'check_speech_id'):
                del self.check_speech_id

    def _handle_key_events(self, event):
        # Allow Ctrl+C and navigation keys
        if (event.state & 0x0004) and (event.keysym.lower() == 'c'):
            return  # Allow copy
        elif event.keysym in ('Right', 'Left', 'Up', 'Down', 'Home', 'End'):
            return  # Allow navigation
        else:
            return 'break'  # Block all other keys

    def _show_context_menu(self, event):
        # Create a menu with only the Copy option
        menu = tk.Menu(self.fullscreen_text, tearoff=0)
        menu.add_command(
            label="Copy",
            command=lambda: self.fullscreen_text.event_generate('<<Copy>>')
        )
        menu.post(event.x_root, event.y_root)

    def on_configure(self, event=None):
        # Update current window dimensions
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Check if window is maximized (with small tolerance)
        maximized = (current_width >= screen_width - 100 and current_height >= screen_height - 100)
        if maximized != self.maximized:
            self.maximized = maximized
            self.update_window_controls()

    def animate_listening_text(self, label, text, index=0):
        if index <= len(text):
            label.config(text=text[:index])
            label.after(100, self.animate_listening_text, label, text, index+1)  # adjust typing speed here
        else:
            # Wait a bit before restarting
            label.after(1000, lambda: self.animate_listening_text(label, text, 0))

    def start_animation(self, event=None):
        if not self.animating:
            self.animating = True
            self.animate_glow()

        if self.placeholder_active:
            self.user_input_box.delete(0, tk.END)
            self.user_input_box.config(fg='white', font=("Arial", 12, 'italic'))
            self.placeholder_active = False

    def stop_animation(self, event=None):
        self.animating = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.inner_frame.config(bg="blue")
        self.frame_1.config(bg="black")
        self.frame_2.config(bg="black")
        self.frame_3.config(bg="black")
        self.frame_4.config(bg="black")
        self.frame_5.config(bg="black")
        self.frame_6.config(bg="black")
        self.frame_7.config(bg="black")
        self.frame_8.config(bg="black")

        if not self.user_input_box.get().strip():
            self.user_input_box.delete(0, tk.END)
            self.user_input_box.insert(0, '     Message...')
            self.user_input_box.config(fg='gray',font=("Arial", 12, 'italic'))
            self.placeholder_active = True
        else:
            self.placeholder_active = False

    def animate_glow(self):
        if not self.animating:
            return

        def get_color(offset, saturation, brightness):
            r, g, b = colorsys.hsv_to_rgb((self.hue + offset) % 1.0, saturation, brightness)
            return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

        # 8 layers from brightest to dimmest
        color1 = get_color(0.00, 1, 1)    # Entry
        color2 = get_color(0.02, 1, 0.80) # Frame 1
        color3 = get_color(0.04, 1, 0.70)  # Frame 2
        color4 = get_color(0.06, 1, 0.60) # Frame 3
        color5 = get_color(0.08, 1, 0.50)  # Frame 4
        color6 = get_color(0.10, 1, 0.40) # Frame 5
        color7 = get_color(0.12, 1, 0.30) # Frame 6
        color8 = get_color(0.14, 1, 0.20) # Frame 7
        color9 = get_color(0.16, 1, 0.10) # Frame 8
        color10 = get_color(0.18, 1, 0.05) # Frame 9
        color11 = get_color(0.20, 1, 0.0) # Frame 10

        self.inner_frame.config(bg=color1)
        self.frame_1.config(bg=color2)
        self.frame_2.config(bg=color3)
        self.frame_3.config(bg=color4)
        self.frame_4.config(bg=color5)
        self.frame_5.config(bg=color6)
        self.frame_6.config(bg=color7)
        self.frame_7.config(bg=color8)
        self.frame_8.config(bg=color9)
        self.frame_9.config(bg=color10)
        self.frame_10.config(bg=color11)

        self.hue = (self.hue + 0.01) % 1.0
        self.after_id = self.root.after(15, self.animate_glow)

    def unfocus_entry(self, event=None):
        self.root.focus()

    def handle_text_input(self, event=None):
        query = self.user_input_box.get().strip()  
        print(f'{query}\n')
        if query == 'Message...' or not query:
            return 'break'

        self.user_input_box.delete(0, tk.END)
        playsound(music_dir)

        display_text = (query[:15] + '...') if len(query) > 15 else query
        self.user_command_label.config(text=f"User :  {display_text}", font=("Arial", 20))
        self.send_message_btn_canvas.pack_forget()
        self.root.after(10, lambda: self.execute_command(query))

    def handel_send_btn_visibility(self, event=None):
        text = self.user_input_box.get().strip()
        if text == "":
            self.send_message_btn_canvas.pack_forget()
        else:
            if not self.send_message_btn_canvas.winfo_ismapped():                
                self.send_message_btn_canvas.pack(side=tk.LEFT, padx=0, pady=0)

    def get_battery_tooltip_text(self):
        battery = psutil.sensors_battery()
        if not battery:
            return "Battery information not available"
        
        percent = battery.percent
        plugged = battery.power_plugged
        status = "Plugged in ⚡" if plugged else "On battery"
        
        # Calculate time left if discharging
        time_info = ""
        if not plugged:
            secs_left = battery.secsleft
            if secs_left == psutil.POWER_TIME_UNLIMITED:
                time_info = "Time left: Calculating..."
            elif secs_left == psutil.POWER_TIME_UNKNOWN:
                time_info = "Time left: Unknown"
            else:
                hours, remainder = divmod(secs_left, 3600)
                minutes, _ = divmod(remainder, 60)
                time_info = f"Time left: {int(hours)}h {int(minutes)}m"
        
        return (
            f"Power: {percent}%\n"
            f"Status: {status}\n"
            f"{time_info}"
        )

    def snap_left(self):
        if self.is_busy:
            return
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        new_width = screen_width // 2
        self.root.geometry(f"{new_width}x{screen_height}+0+0")
        self.maximized = False
        self.update_window_controls()
        self.root.update_idletasks()  # Force UI refresh
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)  

    def snap_right(self):
        if self.is_busy:
            return
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        new_width = screen_width // 2
        x_position = screen_width - new_width
        self.root.geometry(f"{new_width}x{screen_height}+{x_position}+0")
        self.maximized = False
        self.update_window_controls()
        self.root.update_idletasks()  # Force UI refresh
        self.message_input_send_mike_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER)  

    def create_chat_history_panel(self):
        border_width = 2  # Match highlightthickness
        panel_y_position = 100  # Changed from 85 to 120 (35 pixels lower)
        panel_height = HEIGHT - panel_y_position - 35   

        self.chat_history_canvas = tk.Canvas(
            self.root,
            bg="black",
            width=CHAT_HISTORY_WIDTH,
            height=panel_height,
            highlightthickness=border_width,
            highlightbackground="blue",
            highlightcolor="cyan",
        )

        # Initial position accounts for border width
        initial_x = -(CHAT_HISTORY_WIDTH + border_width*2)
        self.chat_history_canvas.place(x=initial_x, y=panel_y_position, width=CHAT_HISTORY_WIDTH)

        self.container = tk.Frame(self.chat_history_canvas, bg="black")
        self.container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Chat.Vertical.TScrollbar",
            gripcount=0,
            background="black",
            troughcolor="black",
            bordercolor="black",
            arrowcolor="black",
            relief="flat",
            width=14
        )
        style.map("Chat.Vertical.TScrollbar",
            background=[("active", "magenta"), ("!active", "cyan")],
            arrowcolor=[("active", "black"), ("!active", "magenta")]
        )
        
        scrollbar = ttk.Scrollbar(
            self.container,
            style="Chat.Vertical.TScrollbar",
            orient="vertical"
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Existing scrollable text setup...
        self.history_text = tk.Text(
            self.container,
            wrap=tk.WORD,
            bg="black",
            fg="red",
            width=CHAT_HISTORY_WIDTH//10 , # Approximate character width
            padx=5,
            pady=5,
            spacing3=5,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.clear_history_btn = tk.Button(
            self.container,
            image=self.delete_chat_icon,
            command=self.clear_chat_history,
            bg="black",
            activebackground="red",
            border=0,
            relief="flat"
        )
        self.clear_history_btn.pack(side=tk.TOP, anchor='ne', padx=(0, 5), pady=(3, 0))
        self.ToolTip(self, self.clear_history_btn, "Clear all\n Chat History")

        self.history_text.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        self.history_text.bind("<Button-3>", self.show_chat_context_menu)
        scrollbar.config(command=self.history_text.yview)

        self.history_text.tag_configure('user', 
            justify='right', 
            background='#0000ff',
            foreground='white',
            font=('Times New Roman', 13),
            relief='raised',
            lmargin1=150,
            lmargin2=150,
            rmargin=10,
            lmargincolor='black',
            spacing1=8,
            spacing3=8,
            borderwidth=0,
        )
        
        self.history_text.tag_configure('bot', 
            justify='left', 
            background='#002040',
            foreground='white',
            font=('Times New Roman', 13),
            relief='raised',
            lmargin1=10,
            lmargin2=10,
            rmargin=150,
            rmargincolor='black',
            spacing1=8,
            spacing3=8,
            borderwidth=0,
        )

        self.history_text.config(pady=5)

        self.history_text.tag_configure('timestamp',
            font=('Arial', 9, 'bold'),
            foreground='#d1d1d1',
            spacing1=10,
        )
        
        self.root.bind('<Button-1>', self.on_root_click)

    def toggle_chat_history(self):
        self.chat_history_open = not self.chat_history_open
        self.animate_chat_panel()

    def animate_chat_panel(self):
        border_width = int(self.chat_history_canvas['highlightthickness'])
        current_x = self.chat_history_canvas.winfo_x()
        target_closed = -(CHAT_HISTORY_WIDTH + border_width*2)
        panel_y_position = 100 
        
        if self.chat_history_open:
            new_x = min(0, current_x + SLIDE_SPEED)
        else:
            new_x = max(target_closed, current_x - SLIDE_SPEED)

        self.chat_history_canvas.place(x=new_x, y=panel_y_position)
        
        if (self.chat_history_open and new_x < 0) or \
        (not self.chat_history_open and new_x > target_closed):
            self.root.after(10, self.animate_chat_panel)

    def update_chat_history(self, user_input, bot_response):
        timestamp = time.strftime("%d-%m-%Y                                  %I:%M:%S %p")
        entry = {
            'time': timestamp,
            'user': user_input,
            'bot': bot_response
        }
        self.chat_history.append(entry)
        
        # Insert formatted messages
        self.history_text.config(state=tk.NORMAL)
        start_index = self.history_text.index(tk.END)


        self.history_text.insert(tk.END, "\n")

        # User message (right-aligned)
        self.history_text.insert(tk.END, f"{user_input}\n\n", 'user')
        self.history_text.insert(tk.END, f"{timestamp}\n", ('user', 'timestamp'))
        
        self.history_text.insert(tk.END, "\n")

        # Bot message (left-aligned)
        self.history_text.insert(tk.END, f"{bot_response}\n", 'bot')
        self.history_text.insert(tk.END, f"{timestamp}\n", ('bot', 'timestamp'))
        
        end_index = self.history_text.index(tk.END)
        entry_index = len(self.chat_history) - 1
        self.history_text.tag_add(f'entry_{entry_index}', start_index, end_index)
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)
        self.save_chat_history()

    def save_chat_history(self):
        try:
            with open(self.chat_file, 'w') as f:
                json.dump(self.chat_history, f, indent=2)
        except Exception as e:
            print(f"Error saving chat: {e}")

    def load_chat_history(self):
        try:
            if os.path.exists(self.chat_file):
                with open(self.chat_file, 'r') as f:
                    self.chat_history = json.load(f)
                    self.history_text.config(state=tk.NORMAL)
                    self.history_text.delete(1.0, tk.END)
                    
                    # Add initial padding at top
                    self.history_text.insert(tk.END, "\n")
                    
                    for i, entry in enumerate(self.chat_history):

                        start_index = self.history_text.index(tk.END)

                        # User message with extra top space
                        self.history_text.insert(tk.END, f"{entry['user']}\n\n", 'user')
                        self.history_text.insert(tk.END, f"{entry['time']}\n", ('user', 'timestamp'))
                        self.history_text.insert(tk.END, "\n")  # Add space between messages
                        
                        # Bot message with extra top space
                        self.history_text.insert(tk.END, f"{entry['bot']}\n", 'bot')
                        self.history_text.insert(tk.END, f"{entry['time']}\n", ('bot', 'timestamp'))
                        self.history_text.insert(tk.END, "\n")  # Add space between chats

                        end_index = self.history_text.index(tk.END)
                        self.history_text.tag_add(f'entry_{i}', start_index, end_index)
                    
                    # Force scroll to bottom after load
                    self.history_text.config(state=tk.DISABLED)
                    self.history_text.see(tk.END)
                    
                    # Update UI before scrolling
                    self.history_text.update_idletasks()
                    
        except Exception as e:
            # print(f"Error loading chat: {e}")
            pass

    def on_root_click(self, event):
        if self.chat_history_open:
            # Get chat history panel bounds
            chat_x = self.chat_history_canvas.winfo_rootx()
            chat_y = self.chat_history_canvas.winfo_rooty()
            chat_width = self.chat_history_canvas.winfo_width()
            chat_height = self.chat_history_canvas.winfo_height()

            # Get history button bounds
            btn_x = self.history_btn.winfo_rootx()
            btn_y = self.history_btn.winfo_rooty()
            btn_width = self.history_btn.winfo_width()
            btn_height = self.history_btn.winfo_height()

            # Check if click is outside both chat panel and history button
            if not (chat_x <= event.x_root <= chat_x + chat_width and
                    chat_y <= event.y_root <= chat_y + chat_height) and \
            not (btn_x <= event.x_root <= btn_x + btn_width and
                    btn_y <= event.y_root <= btn_y + btn_height):
                self.toggle_chat_history()

    def show_chat_context_menu(self, event):
        index = self.history_text.index(f"@{event.x},{event.y}")
        tags = self.history_text.tag_names(index)
        entry_tag = None
        is_user = False
        is_bot = False
        
        for tag in tags:
            if tag.startswith('entry_'):
                entry_tag = tag
            elif tag == 'user':
                is_user = True
            elif tag == 'bot':
                is_bot = True
        
        if not entry_tag:
            return
        
        try:
            entry_index = int(entry_tag.split('_')[1])
        except:
            return
        
        if entry_index < 0 or entry_index >= len(self.chat_history):
            return
        
        self.current_entry_index = entry_index
        self.current_is_user = is_user
        self.current_is_bot = is_bot

        current_theme = self.THEMES[self.current_theme_index]
        
        menu = tk.Menu(self.history_text,
                            tearoff=0, 
                            background=current_theme['bg'], 
                            foreground=current_theme['timestamp'],
                            border=0,
                            activebackground=current_theme['user_bg'],
                            activeforeground='white', 
                            borderwidth=0,
                        )
        menu.add_command(label="Copy", command=self.copy_chat_message)
        menu.add_command(label="Delete", command=self.delete_chat_entry)
        theme_submenu = tk.Menu(menu, tearoff=0,)
        for idx, theme in enumerate(self.THEMES):  # THEMES should be accessible here (might need to move it to class level)
            theme_submenu.add_command(
                label=theme['name'],
                command=lambda idx=idx: self.apply_selected_theme(idx),
                background=current_theme['bg'],
                foreground=current_theme['timestamp'],
                activebackground=theme['user_bg']
            )
        menu.add_cascade(label="Theme", menu=theme_submenu)
        menu.bind("<Enter>", lambda e: self.update_menu_colors(menu, current_theme))
        menu.bind("<Leave>", lambda e: self.update_menu_colors(menu, current_theme))
        menu.post(event.x_root, event.y_root)

    def copy_chat_message(self):
        if not hasattr(self, 'current_entry_index'):
            return
        entry = self.chat_history[self.current_entry_index]
        if self.current_is_user:
            text = entry['user']
        elif self.current_is_bot:
            text = entry['bot']
        else:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text.strip())

    def delete_chat_entry(self):
        if not hasattr(self, 'current_entry_index'):
            return
        del self.chat_history[self.current_entry_index]
        self.save_chat_history()
        self.load_chat_history()

    def clear_chat_history(self):
        # Clear from memory and text widget
        self.chat_history = []
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # Remove content from JSON file
        try:
            with open(self.chat_file, 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Error clearing chat file: {e}")

    def apply_selected_theme(self, theme_index):
        self.current_theme_index = theme_index
        current_theme = self.THEMES[self.current_theme_index]
                
        # Apply new theme settings
        self.chat_history_canvas.config(
            bg=current_theme['bg'],
            highlightbackground=current_theme['highlightbackground'],
            highlightcolor=current_theme['highlightcolor']
        )
        
        # Update text tags
        self.history_text.tag_configure('user', background=current_theme['user_bg'])
        self.history_text.tag_configure('bot', background=current_theme['bot_bg'])
        self.history_text.tag_configure('timestamp', foreground=current_theme['timestamp'])
        
        self.history_text.update_idletasks()

    def animate_theme_transition(self, from_color, to_color):
        # Smooth color transition animation
        steps = 10
        for i in range(steps+1):
            blend = i/steps
            r = int((1-blend)*int(from_color[1:3],16) + blend*int(to_color[1:3],16))
            g = int((1-blend)*int(from_color[3:5],16) + blend*int(to_color[3:5],16))
            b = int((1-blend)*int(from_color[5:7],16) + blend*int(to_color[5:7],16))
            interim_color = f"#{r:02x}{g:02x}{b:02x}"
            self.chat_history_canvas.config(bg=interim_color)
            self.container.config(bg=interim_color)
            self.root.update_idletasks()
            time.sleep(0.02)

    def update_menu_colors(self, menu, theme):
        # Update menu colors in real-time
        menu.configure(
            bg=theme['bg'],
            fg=theme['timestamp'],
            activebackground=theme['user_bg']
        )
        for item in menu.winfo_children():
            if isinstance(item, tk.Menu):
                item.configure(
                    bg=theme['bg'],
                    fg=theme['timestamp'],
                    activebackground=theme['bot_bg']
                )

    def toggle_brightness_panel(self):
        self.brightness_panel_open = not self.brightness_panel_open
        self.animate_brightness_panel()

    def animate_brightness_panel(self):
        panel_height = brightness_panel_height
        highlight = self.brightness_highlight_thickness
        target_y_open = self.battery_bar.winfo_y() + self.battery_bar.winfo_height() + 15
        current_y = self.brightness_panel.winfo_y()
        
        if self.brightness_panel_open:
            final_y = target_y_open
            if current_y < final_y:
                new_y = min(final_y, current_y + brightness_panel_speed)
                if new_y + brightness_panel_speed >= final_y:
                    new_y = final_y
                self.brightness_panel.place(
                                            x=self.brightness_btn.winfo_x() - 75,
                                            y=new_y,
                                            )
                self.root.after(10, self.animate_brightness_panel)
        else:
            final_y = - (panel_height + 2 * highlight)
            if current_y > final_y:
                new_y = max(final_y, current_y - brightness_panel_speed)
                if new_y - brightness_panel_speed <= final_y:
                    new_y = final_y
                self.brightness_panel.place(y=new_y)
                self.root.after(10, self.animate_brightness_panel)

        # Force final position after animation completes
        if not self.brightness_panel_open and current_y == final_y:
            self.brightness_panel.place_forget()
                
    def close_brightness_panel(self, event):
        if self.brightness_panel_open:
            # Get panel bounds in screen coordinates
            panel_x = self.brightness_panel.winfo_rootx()
            panel_y = self.brightness_panel.winfo_rooty()
            panel_width = self.brightness_panel.winfo_width()
            panel_height = self.brightness_panel.winfo_height()

            # Get button bounds in screen coordinates
            btn_x = self.brightness_btn.winfo_rootx()
            btn_y = self.brightness_btn.winfo_rooty()
            btn_width = self.brightness_btn.winfo_width()
            btn_height = self.brightness_btn.winfo_height()

            # Check if click is outside both elements
            if not (panel_x <= event.x_root <= panel_x + panel_width and
                    panel_y <= event.y_root <= panel_y + panel_height) and \
            not (btn_x <= event.x_root <= btn_x + btn_width and
                    btn_y <= event.y_root <= btn_y + btn_height):
                self.brightness_panel_open = False
                self.animate_brightness_panel()

    def set_knob_position(self):
        y = 350 - ((self.current_brightness / 100) * 300)
        line_x = 100
        knob_radius = 10
        
        self.brightness_panel.coords("shadow",
            line_x - knob_radius - 2, y - knob_radius - 2,
            line_x + knob_radius + 2, y + knob_radius + 2
        )
        self.brightness_panel.coords("knob",
            line_x - knob_radius, y - knob_radius,
            line_x + knob_radius, y + knob_radius
        )
        self.brightness_label.config(text=f"{self.current_brightness}%")

    def on_brightness_drag(self, event):
        y = max(50, min(350, event.y))
        line_x = 100
        knob_radius = 10
        
        # Update knob position
        self.brightness_panel.coords("shadow",
            line_x - knob_radius - 2, y - knob_radius - 2,
            line_x + knob_radius + 2, y + knob_radius + 2
        )
        self.brightness_panel.coords("knob",
            line_x - knob_radius, y - knob_radius,
            line_x + knob_radius, y + knob_radius
        )
        
        # Calculate and set brightness
        self.current_brightness = int((350 - y) / 300 * 100)
        try:
            sbc.set_brightness(self.current_brightness, display=0)
        except Exception as e:
            print(f"Brightness error: {e}")
        self.brightness_label.config(text=f"{self.current_brightness}%")



    def execute_command(self, text):
        threading.Thread(target=self.command_handler.handle_command, args=(text,), daemon=True).start()
        
    







if __name__ == "__main__":
    root = tk.Tk()
    app = MainATLAS(root)
    root.mainloop()





