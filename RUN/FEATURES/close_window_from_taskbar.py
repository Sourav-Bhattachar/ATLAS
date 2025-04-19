import pyautogui as p
import pygetwindow as gw
from RUN.FEATURES.remove_words import remove_words

def close_window(query):
    words_to_remove = ['atlas','please','close','the','window','tab']
    query = remove_words(query, words_to_remove)

    ordinal_replacements = {
        'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5',
        'sixth': '6', 'seventh': '7', 'eight': '8', 'ninth': '9',
        '1st': '1', '2nd': '2', '3rd': '3', '4th': '4', '5th': '5',
        '6th': '6', '7th': '7', '8th': '8', '9th': '9'
    }
    for word, num in ordinal_replacements.items():
        query = query.replace(word, num)

    try:
        x = int(query)
    except ValueError:
        return "Error: Invalid window number."
    
    original_window = gw.getActiveWindow()

    try:        
        # Press Win+X to focus the taskbar window
        p.hotkey('win', str(x))
        p.sleep(0.5)  # Wait for the window to activate

        # Check if the active window changed
        new_window = gw.getActiveWindow()
        if new_window != original_window:
            p.sleep(0.3)
            p.hotkey('alt', 'f4')
            return "Done, Sir!"
        else:
            return f"Sorry, Window {x} does not exist in the taskbar."
    except Exception as e:
        return f"Error: {str(e)}"