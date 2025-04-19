import pyautogui


def sleep():
    pyautogui.hotkey('win','x')
    pyautogui.sleep(0.5)
    pyautogui.press('u')
    pyautogui.sleep(0.5)
    pyautogui.press('s') 