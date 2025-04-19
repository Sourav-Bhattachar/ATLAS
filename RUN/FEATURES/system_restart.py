import pyautogui 

def restart():
    pyautogui.hotkey('win','x')
    pyautogui.sleep(0.5)
    pyautogui.press('u')
    pyautogui.sleep(0.5)
    pyautogui.press('r') 
    