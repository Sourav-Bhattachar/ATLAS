import pygetwindow as gw
import time
import pyautogui

def get_brave_window_position(query):
    brave_windows = [win for win in gw.getWindowsWithTitle('YouTube') if 'Brave' in win.title]

    if brave_windows:
        win = brave_windows[0]

        if win.isMinimized:
            win.restore()
            time.sleep(0.1)
        brave_windows[0].activate()
        time.sleep(0.2)

        if ('full' in query and 'screen' in query) or 'maximise' in query or 'maximize' in query:
            pyautogui.press('f')
            return "Video Full Screened!"
        elif 'minimize the' in query or 'minimise the' in query or 'mini the' in query:
            pyautogui.press('f')
            return "Video minimised!"
        elif 'pause' in query:
            pyautogui.press('k')
            return "Video paused!"
        elif "play" in query or 'resume' in query:
            pyautogui.press('k')
            return "Video played!"
        elif "unmute" in query:
            pyautogui.press('m')
            return "Video unmuted!"
        elif "mute" in query:
            pyautogui.press('m')
            return "Video muted!"
    else:
        return "No Youtube window found in Brave browser."
