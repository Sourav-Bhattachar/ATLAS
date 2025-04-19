import pyautogui as p
from RUN.FEATURES.remove_words import remove_words

def open_window(query):
    words_to_remove = ['atlas','please','open','the','window','tab']
    query = remove_words(query, words_to_remove)

    query = query.replace('first','1')
    query = query.replace('second','2')
    query = query.replace('third','3')
    query = query.replace('fourth','4')
    query = query.replace('phone','4')
    query = query.replace('fifth','5')
    query = query.replace('sixth','6')
    query = query.replace('seventh','7')
    query = query.replace('eight','8')
    query = query.replace('ninth','9')

    query = query.replace('1st','1')
    query = query.replace('2nd','2')
    query = query.replace('3rd','3')
    query = query.replace('4th','4')
    query = query.replace('5th','5')
    query = query.replace('6th','6')
    query = query.replace('7th','7')
    query = query.replace('8th','8')
    query = query.replace('9th','9')

    x= int(query)

    if x == 2:
        p.hotkey('win','2')
        
    if x == 3:
        p.hotkey('win','3')
     
    elif x == 4:
        p.hotkey('win','4')
    
    elif x == 5:
        p.hotkey('win','5')
        
    elif x == 6:
        p.hotkey('win','6')

    elif x == 7:
        p.hotkey('win','7')
        
    elif x == 8:
        p.hotkey('win','8')

    elif x == 9:
        p.hotkey('win','9')
        
    return 'Done, Sir!'