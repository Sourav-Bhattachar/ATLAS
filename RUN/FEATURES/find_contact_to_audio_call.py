import os
import csv
import time
import pyautogui as p

# Configuration (adjust these if your CSV uses different column names)
CSV_FILENAME =  r'RUN\FEATURES\contacts.csv'
NAME_COLUMN = 'First Name'  # Change to match your CSV's name column
MOBILE_COLUMN = 'Mobile Number'  # Change to match your CSV's mobile column

def find_contact_to_audio_call(query):
    # Get user input and normalize case
    search_name = query
    search_lower = search_name.lower()  # For case-insensitive comparison
    
    try:
        with open(CSV_FILENAME, 'r') as file:
            reader = csv.reader(file)

            # Read and clean headers
            headers = [header.strip() for header in next(reader)]
            
            # Find column indices
            try:
                name_index = headers.index(NAME_COLUMN)
                mobile_index = headers.index(MOBILE_COLUMN)
            except ValueError as e:
                print(f"Error: Column '{e.args[0]}' not found in CSV")
                return

            # Search through rows
            found = False
            for row in reader:
                if len(row) > max(name_index, mobile_index):
                    original_name = row[name_index].strip()
                    # Case-insensitive comparison
                    if original_name.lower() == search_lower:
                        print(f"\nName: {original_name}")
                        print(f"Mobile: {row[mobile_index].strip()}")                        
                        start_whatsapp_audio_call(row[mobile_index].strip())
                        return f"Starting audio call to {original_name}. Please wait" 
        
            if not found:
                print(f"'{search_name}' not found in the contacts.")
                return f"'{search_name}' not found in the contacts."


    except FileNotFoundError:
        print(f"Error: File '{CSV_FILENAME}' not found")



def start_whatsapp_audio_call(phone_number):
    whatsapp_uri = f"whatsapp://send?phone={phone_number}"
    os.startfile(whatsapp_uri)
    time.sleep(5)
    for i in range(11): # press 10 tab to navaigate the audio call button
        p.press('tab')
        time.sleep(0.1)
    p.sleep(0.2)
    p.press('enter')
