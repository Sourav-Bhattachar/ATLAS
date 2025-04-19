import pyttsx3
import queue
import threading

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 200)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.speech_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.is_running = False

    def tts_worker(self):
        while not self.stop_event.is_set():
            try:
                text = self.speech_queue.get(timeout=1)
                with self.lock:
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.engine.stop()  # Add proper cleanup
            except queue.Empty:
                continue

    def start(self):
        self.tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
        self.tts_thread.start()

    def speak(self, text):
        if not self.stop_event.is_set() and not self.is_running:
            with self.lock:
                self.is_running = True
                self.speech_queue.put(text)
                self.is_running = False
                
    def stop(self):
        self.stop_event.set()
        with self.lock:
            self.engine.stop()
        self.tts_thread.join()

# Initialize singleton instance
tts_controller = TTSManager()
tts_controller.start()