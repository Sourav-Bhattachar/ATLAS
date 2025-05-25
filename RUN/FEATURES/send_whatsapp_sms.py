import os
import csv
import time
import pyautogui as p
import urllib.parse
CSV_FILENAME =  r'RUN\FEATURES\contacts.csv'
NAME_COLUMN = 'First Name'
MOBILE_COLUMN = 'Mobile Number'

def find_contact_to_send_sms(contact_query, message):
    search_name = contact_query
    search_lower = search_name.lower()

    try:

        with open(CSV_FILENAME, 'r') as file:
            reader = csv.reader(file)
            headers = [header.strip() for header in next(reader)]

            try:
                name_index = headers.index(NAME_COLUMN)
                mobile_index = headers.index(MOBILE_COLUMN)

            except ValueError as e:
                return f"Error: Column '{e.args[0]}' not found."
            for row in reader:

                if len(row) > max(name_index, mobile_index):
                    original_name = row[name_index].strip()

                    if original_name.lower() == search_lower:
                        phone_number = row[mobile_index].strip()
                        send_sms(phone_number, message)
                        return f"Successfully message sent to {original_name}."
            return f"Contact '{search_name}' not found."

    except FileNotFoundError:
        return f"Contacts file not found."

def send_sms(phone_number, message):
    encoded_message = urllib.parse.quote(message)
    whatsapp_uri = f"whatsapp://send?phone={phone_number}&text={encoded_message}"
    os.startfile(whatsapp_uri)
    time.sleep(5)
    p.press('enter')
    p.sleep(0.2)
    p.hotkey('alt', 'f4')
