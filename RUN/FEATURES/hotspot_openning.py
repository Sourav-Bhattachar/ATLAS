import pyautogui as p

def hotspot_openning():
    p.press('browsersearch')
    p.sleep(0.5)
    p.write('hotspot',0.3)
    p.press('enter')
    p.sleep(5)
    p.moveTo(1720,180)
    p.sleep(0.2)
    p.leftClick()
    p.sleep(2)
    p.hotkey('alt','f4')
    return 'Done, Sir!'