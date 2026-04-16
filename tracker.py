import threading
import time
from datetime import datetime

from logger import log_event, log_app_usage
from pynput import mouse, keyboard
import pygetwindow as gw


class ActivityTracker:
    def __init__(self):
        self.running = False
        self.last_activity = time.time()

        self.current_window = None
        self.window_start_time = None

        self.typed_text = ""   # 🔥 store meaningful typing

    def start(self):
        self.running = True
        log_event("session", "Session started")

        threading.Thread(target=self.track_active_window, daemon=True).start()
        threading.Thread(target=self.track_idle, daemon=True).start()

        self.mouse_listener()
        self.keyboard_listener()

    def stop(self):
        self.running = False

        #  Save last app usage before stopping
        if self.current_window and self.window_start_time:
            end_time = datetime.now()
            duration = (end_time - self.window_start_time).seconds

            log_app_usage(
                self.current_window,
                self.window_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_time.strftime("%Y-%m-%d %H:%M:%S"),
                duration
            )

        log_event("session", "Session ended")

    #  Mouse (minimal logging)
    def mouse_listener(self):
        def on_click(x, y, button, pressed):
            if pressed and self.running:
                self.last_activity = time.time()
                #  Removed noisy logging

        listener = mouse.Listener(on_click=on_click)
        listener.daemon = True
        listener.start()

    #  Keyboard (SMART logging)
    def keyboard_listener(self):
        def on_press(key):
            if not self.running:
                return

            self.last_activity = time.time()

            try:
                # Normal characters
                self.typed_text += key.char
            except:
                # Special keys handling
                if key == keyboard.Key.space:
                    self.typed_text += " "

                elif key == keyboard.Key.enter:
                    if self.typed_text.strip():
                        log_event("text", f"User typed: {self.typed_text}")
                    self.typed_text = ""

                elif key == keyboard.Key.backspace:
                    self.typed_text = self.typed_text[:-1]

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()

    # Window tracking (clean + accurate)
    def track_active_window(self):
        while self.running:
            try:
                window = gw.getActiveWindow()
                if window:
                    title = window.title.strip()

                    if title and title != self.current_window:

                        # Save previous app usage
                        if self.current_window and self.window_start_time:
                            end_time = datetime.now()
                            duration = (end_time - self.window_start_time).seconds

                            log_app_usage(
                                self.current_window,
                                self.window_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                                end_time.strftime("%Y-%m-%d %H:%M:%S"),
                                duration
                            )

                        # Switch to new window
                        self.current_window = title
                        self.window_start_time = datetime.now()

                        log_event("window", f"Opened {title}")

            except Exception:
                pass

            time.sleep(2)

    #  Idle tracking (clean)
    def track_idle(self):
        while self.running:
            idle_time = time.time() - self.last_activity

            if idle_time > 60:
                minutes = int(idle_time / 60)
                log_event("idle", f"User idle for {minutes} minutes")
                self.last_activity = time.time()

            time.sleep(10)