import os
import csv
import time
import pyautogui as p
CSV_FILENAME =  r'RUN\FEATURES\contacts.csv'
NAME_COLUMN = 'First Name'
MOBILE_COLUMN = 'Mobile Number'

def find_contact_deatils(query):
    search_name = query
    search_lower = search_name.lower()

    try:

        with open(CSV_FILENAME, 'r') as file:
            reader = csv.reader(file)
            headers = [header.strip() for header in next(reader)]

            try:
                name_index = headers.index(NAME_COLUMN)
                mobile_index = headers.index(MOBILE_COLUMN)

            except ValueError as e:
                print(f"Error: Column '{e.args[0]}' not found in CSV")
                return
            found = False
            for row in reader:

                if len(row) > max(name_index, mobile_index):
                    original_name = row[name_index].strip()

                    if original_name.lower() == search_lower:
                        print(f"\nName: {original_name}")
                        print(f"Mobile: {row[mobile_index].strip()}")
                        return f"Name: {original_name}.\nContact number: {row[mobile_index].strip()}"

            if not found:
                print(f"'{search_name}' not found in the contacts.")
                return f"'{search_name}' not found in the contacts."

    except FileNotFoundError:
        print(f"Error: File '{CSV_FILENAME}' not found")
