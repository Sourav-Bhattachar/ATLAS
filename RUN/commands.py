import calendar
import json
import schedule
import os
import time
import random
import periodictable
import re
import pyautogui
import threading
import tkinter as tk
import speech_recognition
from multiprocessing import Process
import webbrowser
from datetime import date
import psutil
from io import BytesIO
import requests
from PIL import Image, ImageTk
import datetime
import screen_brightness_control as sbc


from RUN.FEATURES.calendar_generator import DynamicCalendarApp
from RUN.FEATURES.internet_speed_test import InternetSpeedometer
from RUN.FEATURES.remove_words import remove_words
from RUN.FEATURES.play_on_youtube import search_youtube
from RUN.FEATURES.taking_screen_shot import screen_shot
from RUN.FEATURES.find_contact_number import find_contact_deatils
from RUN.FEATURES.find_contact_to_video_call import find_contact_to_video_call
from RUN.FEATURES.find_contact_to_audio_call import find_contact_to_audio_call
from RUN.FEATURES.send_whatsapp_sms import find_contact_to_send_sms
from RUN.FEATURES.hotspot_openning import hotspot_openning
from RUN.FEATURES.open_window_from_taskbar import open_window
from RUN.FEATURES.close_window_from_taskbar import close_window
from RUN.FEATURES.periodic_table_generator import create_periodic_table, show_element_info
from RUN.FEATURES.periodic_table_generator import create_periodic_table, show_element_info
from RUN.FEATURES.youtube_video_full_screen import get_brave_window_position
from RUN.FEATURES.snake_game import snake_game
from RUN.FEATURES.flappy_bird_game import flappy_game
from RUN.FEATURES.country_details import country_details
from RUN.FEATURES.get_temperature import get_temperature
from RUN.FEATURES.click_photo import take_photo
from RUN.FEATURES.chemistry_element_iupac_name import element_details
from RUN.FEATURES.atlas_memory import write_unique_line
from RUN.FEATURES.memory_recall import recall
from RUN.FEATURES.system_shut_down import shut_down
from RUN.FEATURES.system_restart import restart
from RUN.FEATURES.system_sleep import sleep
from RUN.FEATURES.lock_screen import lock


JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"


def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 2
        r.pause_threshold = 1
        audio = r.listen(source,0,4)
    try:
        print("Understanding...")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
        time.sleep(2)
    except Exception as e:
        print("Say that again")
        return "None"
    return query.lower()



class CommandHandler:
    def __init__(self, atlas_instance):
        self.atlas = atlas_instance  
        self.reminders_file = r'RUN\FEATURES\reminders.json'
        self.todos_file = r'RUN\FEATURES\todos.json'

    def false_command(self):
        pass

    def parse_calendar_command(self, query):
        query = query.lower()
        year = None
        month = None
        
        # Extract year (look for a 4-digit number)
        year_matches = re.findall(r'\b\d{4}\b', query)
        if year_matches:
            year = int(year_matches[0])
        
        # Extract month names
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        for month_name, month_num in months.items():
            if month_name in query:
                month = month_num
                break
        
        return year, month

    def extract_element_name(self, query):
        # Match patterns like "open lithium on periodic table" or "show sodium in periodic table"
        match = re.search(
            r'(?:open|show|display)\s+(?:the\s+)?(.+?)\s+(?:on|in|at|from|to)\s+(?:the\s+)?periodic\s+table',
            query,
            re.IGNORECASE
        )
        if not match:
            match = re.search(
                r'periodic\s+table\s+(?:of\s+)?(.+)',
                query,
                re.IGNORECASE
            )
        return match.group(1).strip().lower() if match else None

    def get_symbol_from_name(self, element_name):
        # Convert element name to symbol using periodictable
        for elem in periodictable.elements:
            if elem.name.lower() == element_name.lower():
                return elem.symbol
        return None

    def _take_message_command(self, contact_name):
        message = takeCommand().lower()
        response_text = find_contact_to_send_sms(contact_name, message)
        self.atlas.root.after(10, self.atlas.update_chat_history, message, response_text)

    def create_flag_window(self, photo, country_name):
        words_to_remove = ['what', 'is','the','country','details','of']
        country_name = remove_words(country_name, words_to_remove)
        flag_window = tk.Toplevel(self.atlas.root)
        flag_window.resizable(False,False)
        flag_window.title(f"Flag of {country_name.capitalize()}")
        
        # Center window
        window_width = 450
        window_height = 300
        screen_width = flag_window.winfo_screenwidth()
        screen_height = flag_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        flag_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Add image label
        label = tk.Label(flag_window, image=photo)
        label.image = photo  # Keep reference
        label.pack(padx=10, pady=10)
        
    def set_reminder(self, text):
        try:
            # Extract time and message
            match = re.search(r'in (\d+) minutes? to (.*)', text)
            if not match:
                return "Invalid reminder format. Please use: 'remind me in X minutes to Y'"
            
            minutes = int(match.group(1))
            message = match.group(2)
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            
            # Save reminder
            reminder = {
                'time': reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
                'message': message
            }
            
            if not os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'w') as f:
                    json.dump([], f)
            
            with open(self.reminders_file, 'r+') as f:
                reminders = json.load(f)
                reminders.append(reminder)
                f.seek(0)
                json.dump(reminders, f)
            
            # Start reminder checker
            self.start_reminder_checker()
            return f"Reminder set for {minutes} minutes from now: {message}"
        except Exception as e:
            return f"Error setting reminder: {str(e)}"

    def start_reminder_checker(self):
        def check_reminders():
            try:
                with open(self.reminders_file, 'r') as f:
                    reminders = json.load(f)
                
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for reminder in reminders[:]:
                    if reminder['time'] <= now:
                        self.atlas.speak(f"Reminder: {reminder['message']}")
                        reminders.remove(reminder)
                
                with open(self.reminders_file, 'w') as f:
                    json.dump(reminders, f)
            
            except Exception as e:
                print(f"Reminder check error: {str(e)}")
        
        # Run every minute
        schedule.every(1).minutes.do(check_reminders)
        threading.Thread(target=self.run_scheduler, daemon=True).start()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def tell_joke(self):
        try:
            response = requests.get(JOKE_API_URL)
            joke = response.json()['joke']
            return f"Here's a joke:\n{joke}"
        except Exception as e:
            return "Why did the joke go to school? To get a little smarter!"

    def get_system_info(self):
        try:
            info = {
                'cpu_usage': f"{psutil.cpu_percent()}%",
                'ram_usage': f"{psutil.virtual_memory().percent}%",
                'disk_usage': f"{psutil.disk_usage('/').percent}%",
                'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
            return (f"System Information:\n"
                    f"CPU Usage: {info['cpu_usage']}\n"
                    f"RAM Usage: {info['ram_usage']}\n"
                    f"Disk Usage: {info['disk_usage']}\n"
                    f"Last Boot: {info['boot_time']}")
        except Exception as e:
            return f"Couldn't get system info: {str(e)}"


    def handle_command(self, text):
        
        def _process_command():
            self.atlas.is_busy = True
            self.atlas.hotword_active = False
            query = text.lower()
            response_text = ""

            try:
                if "on youtube" in query and 'play' in query:
                    try:
                        response_text = search_youtube(query)
                        
                    except Exception as e:
                        response_text = self.atlas.chat_bot(query)
                    
                    finally:
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif "screenshot" in query or "screen shot" in query:
                    try:
                        response_text = screen_shot()
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                    except:
                        print("Error in taking screenshot")                                     

                elif 'video call' in query:
                    words_to_remove = ['atlas','create','do','please', 'make', 'a', 'tu', 'to', 'phone','sms', 'call', 'send', 'message', 'wahtsapp', 'video', 'audio']
                    query = remove_words(query, words_to_remove)
                    response_text = find_contact_to_video_call(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'audio call' in query:
                    words_to_remove = ['atlas','create','do','please', 'make', 'a', 'tu', 'to', 'phone','sms', 'call', 'send', 'message', 'wahtsapp', 'video', 'audio']
                    query = remove_words(query, words_to_remove)
                    response_text = find_contact_to_audio_call(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif 'hotspot' in query or 'Hotspot' in query:
                    response_text = hotspot_openning()
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ('who' in query or 'what' in query) and 'the first' in query:
                    response_text = self.atlas.chat_bot(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'all' in query and ('close' in query or 'minimize' in query or 'minimise' in query ):
                    pyautogui.hotkey('win','d')
                    response_text = "All windows minimized"
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                                
                elif 'calendar' in query and ('show' in query or 'open' in query or 'create' in query or 'see' in query or 'generate' in query):
                    try:
                        parsed_year, parsed_month = self.parse_calendar_command(query)
                        if parsed_year is None:
                            raise ValueError("Please specify a year.")
                        
                        # Create a Toplevel window
                        top = tk.Toplevel(self.atlas.root)
                        top.title("Calendar")
                        if parsed_month is not None:
                            window_width, window_height = 400, 350

                        else:
                            window_width, window_height = 1000, 790
                        
                        screen_width = top.winfo_screenwidth()
                        screen_height = top.winfo_screenheight()
                        x = (screen_width - window_width) // 2
                        y = (screen_height - window_height) // 2
                        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

                        # Initialize the DynamicCalendarApp
                        DynamicCalendarApp(top, parsed_year, parsed_month)
                        
                        response_text = f"Opened calendar for {parsed_year}"
                        if parsed_month is not None:
                            response_text += f", month {calendar.month_name[parsed_month]}"
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                    except Exception as e:
                        response_text = f"Error: {str(e)}"
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                   
                elif 'periodic table' in query.lower():
                    element_name = self.extract_element_name(query)
                    
                    if element_name:
                        try:
                            # Use periodictable's built-in name matching
                            element = getattr(periodictable, element_name.lower())
                            symbol = element.symbol                            
                            table_window = create_periodic_table(self.atlas.root)
                            table_window.after(100, lambda: show_element_info(symbol)) 
                            density = getattr(element, 'density', None)
                            density_value = f"{density} g/cm³" if density else "N/A"
                            response_text = f"Name {element.name.capitalize()}.\n Atomic Number: {element.number}.\n Atomic Mass: {element.mass:.3f} amu.\n Density: {density_value}."
                            
                        except AttributeError:
                            response_text = f"Element '{element_name}' not found in periodic table"
                    else:
                        # Open periodic table without specific element
                        create_periodic_table(self.atlas.root)
                        response_text = "Opened periodic table"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif  ('tab' in query or 'window' in query) and 'open' in query:
                    response_text = open_window(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'close' in query and ('tab' in query or 'window' in query):
                    response_text = close_window(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'who are you' in query or 'who r u' in query or 'your name' in query or 'hu r u' in query  or 'hu are you' in query:
                    response_text = "My name is Atlas, your personal assistant. How can I help you today?"
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'contact' in query and ('number' in query or 'details' in query):
                    words_to_remove = ['atlas','what','is','the','contact','number','of','details']
                    query = remove_words(query, words_to_remove)
                    response_text = find_contact_deatils(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'message' in query or 'sms' in query:
                    words_to_remove = ['atlas','create','do','please', 'make', 'a', 'tu', 'to', 'phone','sms', 'call', 'send', 'message', 'wahtsapp', 'video', 'audio']
                    contact_name = remove_words(query, words_to_remove)
                    response_text = 'What message to send?'
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                    
                    self.atlas.speak(response_text, callback=lambda: [
                        threading.Thread(target=self._take_message_command, args=(contact_name,), daemon=True
                    ).start()])

                elif "internet speed" in query or "network speed" in query:
                    try:
                        # Create Toplevel window
                        top = tk.Toplevel(self.atlas.root)
                        top.title("Internet Speed Test")
                        window_width, window_height = 1000, 500
                        
                        # Center window
                        screen_width = top.winfo_screenwidth()
                        screen_height = top.winfo_screenheight()
                        x = (screen_width - window_width) // 2
                        y = (screen_height - window_height) // 2
                        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

                        # Define callback for results
                        def speed_test_callback(download, upload):
                            response_text = (f"Speed Test Completed!\n"
                                            f"Download speed: {download:.2f} Mbps\n"
                                            f"Upload speed: {upload:.2f} Mbps")
                            self.atlas.update_chat_history(text, response_text)
                            self.atlas.root.after(10, lambda: threading.Thread(
                                target=self.atlas.speak,
                                args=(response_text,),
                                kwargs={'callback': self.false_command},
                                daemon=True
                            ).start())
                            return
                        # Initialize speed test with callback
                        InternetSpeedometer(top, speed_test_callback)
                        response_text = "Starting internet speed test, please wait..."
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                        
                    except Exception as e:
                        response_text = f"Speed test failed: {str(e)}"
                        self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "tired" in query :
                    webbrowser.open(r'ATLAS_UI_VIDEO_AUDIO\f_song.mp3')
                    response_text = (" Dont worry sir, please relax.\nI will be Playing your favourite songs")
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ('full' in query and 'screen' in query) or 'maximise' in query or 'maximize' in query:
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'minimize the' in query or 'minimise the' in query or 'mini the' in query:
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'play a game' in query or 'play the game' in query or 'play some game' in query or 'try some game' in query or 'try a game' in query or 'try the game' in query:
                    game_choice = random.choice(['snake_game', 'flappy_game']) 

                    if game_choice == 'snake_game':
                        try:
                            game_process = Process(target=snake_game)
                            game_process.start()
                            response_text = "Ok, let's play a random snake game...\nPlease wait..."
                        except Exception as e:
                            response_text = f"Couldn't start snake game: {str(e)}"
                    else:
                        try:
                            game_process = Process(target=flappy_game)
                            game_process.start()
                            response_text = "Ok, let's play a random Flappy Bird game...\nPlease wait..."
                        except Exception as e:
                            response_text = f"Couldn't start Flappy Bird game: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'play the snake game' in query or 'play a snake game' in query:
                    try:
                        game_process = Process(target=snake_game)
                        game_process.start()
                        response_text = "Ok, let's play a snake game...\nPlease wait..."
                    except Exception as e:
                        response_text = f"Couldn't start game: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "flappy bird game" in query:
                    try:
                        game_process = Process(target=flappy_game)
                        game_process.start()
                        response_text = "Ok, let's play a Flappy Bird game...\nPlease wait..."
                    except Exception as e:
                        response_text = f"Couldn't start game: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'favourite song' in query or 'favourite music' in query or 'me happy' in query:
                    response_text = ("Ok sir, please wait. I will be Playing your favourite songs")
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                    webbrowser.open(r'ATLAS_UI_VIDEO_AUDIO\f_song.mp3')

                elif "open" in query:
                    words_to_remove = ['atlas','please','open', 'lets', 'let\'s', 'from', 'desktop']
                    query = remove_words(query, words_to_remove)
                    response_text = f'openning {query}, please wait...'
                    self.atlas.root.after(1, self.atlas.update_chat_history, text, response_text)
                    pyautogui.press("super")
                    pyautogui.sleep(1)
                    pyautogui.typewrite(query)
                    pyautogui.sleep(0.3)
                    pyautogui.press("enter")  

                elif 'unmute the system' in query or 'unmute the laptop' in query or 'unmute my laptop' in query:
                    response_text = 'ok, the system is unmuting...'
                    self.atlas.root.after(1, self.atlas.update_chat_history, text, response_text)
                    pyautogui.press('volumemute')

                elif 'mute the system' in query or 'mute the laptop' in query or 'mute my laptop' in query:
                    response_text = 'ok, the system is muting...'
                    self.atlas.root.after(1, self.atlas.update_chat_history, text, response_text)
                    pyautogui.press('volumemute')

                elif "pause" in query:
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "play" in query or 'resume' in query:
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "unmute the video" in query or "unmute the song" in query or "unmute the youtube video" in query or "unmute the youtube song" in query:
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "mute the video" in query or "mute the song" in query or "mute the youtube video" in query or "mute the youtube song" in query :
                    response_text = get_brave_window_position(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif "volume" in query and "up" in query and ('for' in query or 'to' in query):
                    words_to_remove = ['atlas','please','turn', 'tern', 'the','to', 'on', 'volume', 'up','for']
                    query = remove_words(query, words_to_remove)
                    query = int(query)
                    try:
                        response_text = f'Ok sir, turning the volume up for {query}'
                        pyautogui.press('volumeup',int(query/2))                        
                    except:
                        response_text = f'Ok sir, turning the volume up for 5'
                        pyautogui.press('volumeup',5)  

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif 'volume' in query and "up" in query:
                    response_text = f'Ok sir, turning the volume up for 5'
                    pyautogui.press('volumeup',5) 
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "volume" in query and "down" in query and ('for' in query or 'to' in query):
                    words_to_remove = ['atlas','please','turn', 'tern', 'the','to', 'on', 'volume', 'down', 'for']
                    query = remove_words(query, words_to_remove)
                    query = int(query)
                    try:
                        response_text = f'Ok sir, turning the volume down for {query}'
                        pyautogui.press('volumedown',int(query/2))                        
                    except:
                        response_text = f'Ok sir, turning the volume down for 5'
                        pyautogui.press('volumedown',5)  

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif 'volume' in query and "down" in query:
                    response_text = f'Ok sir, turning the volume down for 5'
                    pyautogui.press('volumedown',5) 
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ('increase' in query or 'up' in query) and 'brightness' in query:
                    try:
                        current = sbc.get_brightness()
                        if current:
                            current = current[0]
                            new = min(current + 10, 100)
                            sbc.set_brightness(new)
                            response_text = f"Brightness increased to {new}%"
                        else:
                            response_text = "Could not retrieve current brightness"
                    except Exception as e:
                        response_text = f"Failed to increase brightness: {str(e)}"
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ('decrease' in query or 'down' in query) and 'brightness' in query:
                    try:
                        current = sbc.get_brightness()
                        if current:
                            current = current[0]
                            new = max(current - 10, 0)
                            sbc.set_brightness(new)
                            response_text = f"Brightness decreased to {new}%"
                        else:
                            response_text = "Could not retrieve current brightness"
                    except Exception as e:
                        response_text = f"Failed to decrease brightness: {str(e)}"
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "date" in query:
                    current_datetime = date.today()
                    response_text = f'Curren date is: {current_datetime}'
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'country details' in query:
                    response_text, flag_url = country_details(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                    def display_flag(image_url):
                        try:
                            # Download image
                            response = requests.get(image_url)
                            img_data = response.content
                            
                            # Create PIL Image and convert for Tkinter
                            img = Image.open(BytesIO(img_data))
                            img = img.resize((400, 250), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            
                            # Create new window in main thread
                            self.atlas.root.after(0, lambda: 
                                self.create_flag_window(photo, query))
                            
                        except Exception as e:
                            print(f"Error loading flag: {e}")

                    if flag_url:
                        threading.Thread(target=display_flag,args=(flag_url,), daemon=True).start()
                    else:
                        self.atlas.speak(response_text)

                elif "calculate" in query:
                    response_text = self.atlas.chat_bot(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ('charge' in query or 'power' in query or 'battery' in query) and ('laptop' in query or 'pc' in query or 'desktop' in query or 'computer' in query):
                    battery = psutil.sensors_battery()
                    if battery is None:
                        response_text = ("No battery information found")

                    percent = battery.percent
                    is_plugged = battery.power_plugged
                    status = "Charging" if is_plugged else "Not charging"
                    response_text = (f"Battery is at {percent}% and is currently {status}.")
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "temperature" in query or 'weather' in query:
                    words_to_remove = ['atlas','please','tell','me','what','is','the','of','temperature','current','weather','in']
                    query = remove_words(query, words_to_remove)
                    response_text = get_temperature(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'remind me' in query: # "Remind me in 15 minutes to check the oven"
                    response_text = self.set_reminder(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                
                elif 'tell me a joke' in query or 'make me laugh' in query:
                    response_text = self.tell_joke()
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'system' in query and ('info' in query or 'information' in query or 'status' in query or 'characteristic' in query):
                    response_text = self.get_system_info()
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "click my photo" in query or "take my photo" in query or "take a photo" in query or "click a photo" in query:
                    try:
                        photo_taking_process = Process(target=take_photo)
                        photo_taking_process.start()
                        response_text = "Ok sir, please wait for a moment, I am taking your photo.\nPress any key to save and close the window"
                    except Exception as e:
                        response_text = f"Couldn't start game: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'iupac' in query or 'molecular' in query or 'weight' in query or 'formula' in query:
                    response_text = element_details(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'time' in query:
                    now = datetime.datetime.now()
                    formatted_time = now.strftime("%I:%M %p")
                    formatted_time = formatted_time.lstrip("0")
                    response_text = (f"The Current Time is: {formatted_time}")  
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "remember that" in query:
                    words_to_remove = ['remember that','atlas','please']
                    query = remove_words(query, words_to_remove)
                    response_text = write_unique_line(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'clear' in query and 'memory' in query:
                    response_text = "Memory cleared"
                    with open(r"RUN\FEATURES\Remember.txt", "w") as file:
                        file.write("")
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "you remember" in query:
                    response_text = recall()
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "exit" in query or "good bye" in query or "goodbye" in query or "bye" in query:
                    now = datetime.datetime.now()
                    current_time = now.time()
                    
                    # Define night time as 10 PM to 5 AM
                    if current_time >= datetime.time(22, 0) or current_time < datetime.time(5, 0):
                        response_text = "Thank you sir, it's a nice conversation, have a good night."
                    else:
                        response_text = "Thank you sir, it's a nice conversation, have a good day."

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
                    
                    self.atlas.root.after(10, lambda: threading.Thread(
                        target=self.atlas.speak,
                        args=(response_text,),
                        kwargs={'callback': self.atlas.on_close},
                        daemon=True
                    ).start())
                    return
                   
                elif ("shutdown" in query or 'shut down' in query )and ('system' in query or 'pc' in query or 'laptop' in query or 'computer' in query or 'desktop' in query or 'screen' in query):
                    now = datetime.datetime.now()
                    current_time = now.time()

                    try:
                        shutdown_process = Process(target=shut_down)
                        shutdown_process.start()
                        if current_time >= datetime.time(22, 0) or current_time < datetime.time(5, 0):
                            response_text = ("Thank you sir, it's a nice conversation, Have a good night")
                        else:
                            response_text = ("Thank you sir, it's a nice conversation, Have a good day")

                    except Exception as e:
                        response_text = f"Couldn't shutdown: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif ("restart" in query or "re start" in query) and ('system' in query or 'pc' in query or 'laptop' in query or 'computer' in query or 'desktop' in query or 'screen' in query):
                    try:
                        restart_process = Process(target=restart)
                        restart_process.start()
                        response_text = "Thank You sir, please wait for me, I am restarting your system"

                    except Exception as e:
                        response_text = f"Couldn't restart: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif "sleep" in query and ('system' in query or 'pc' in query or 'laptop' in query or 'computer' in query or 'desktop' in query or 'screen' in query):
                    try:
                        sleep_process = Process(target=sleep)
                        sleep_process.start()
                        response_text = 'Ok sir, the system is sleeping...'

                    except Exception as e:
                        response_text = f"Couldn't sleep: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                elif 'lock' in query and ('system' in query or 'pc' in query or 'laptop' in query or 'computer' in query or 'desktop' in query or 'screen' in query):
                    try:
                        lock_process = Process(target=lock)
                        lock_process.start()
                        response_text = 'Ok sir, the system is locking...'

                    except Exception as e:
                        response_text = f"Couldn't lock: {str(e)}"

                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

                else:
                    response_text = self.atlas.chat_bot(query)
                    self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)

            except Exception as e:
                response_text = f"Error: {str(e)}"
                self.atlas.root.after(10, self.atlas.update_chat_history, text, response_text)
            

            # Update UI and speak response
            if len(response_text.split()) >= 1:
                self.atlas.root.after(10, lambda: [
                    self.atlas.create_fullscreen_text(),
                    self.atlas.fullscreen_text.delete(1.0, 'end'),
                    self.atlas.fullscreen_text.insert('end', response_text + '\n\n', 'response'),
                    self.atlas.fullscreen_text.see(tk.END),
                    threading.Thread(
                        target=self.atlas.speak,
                        args=(response_text,),
                        kwargs={'callback': lambda: self.atlas.root.after(0, self.atlas.schedule_label_clear)},
                        daemon=True
                    ).start()
                ])
           
            else:
                self.atlas.root.after(0, lambda: [
                    self.atlas.bot_response_label.config(text=f"Atlas:  {response_text}"),
                    threading.Thread(
                        target=self.atlas.speak,
                        args=(response_text,),
                        kwargs={'callback': lambda: self.atlas.root.after(0, self.atlas.schedule_label_clear)},
                        daemon=True
                    ).start()
                ])

        threading.Thread(target=_process_command, daemon=True).start()

