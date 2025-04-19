import pyautogui

def screen_shot():
    img = pyautogui.screenshot('ss.png')
    img.show("ss.png")
    img.save('ss.png')
    return 'Done, Sir!'