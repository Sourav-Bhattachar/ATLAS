from RUN.FEATURES.remove_words import remove_words
import re

file_path = r'RUN\FEATURES\Remember.txt'

def write_unique_line(new_line):
    # Define replacement mappings
    replacement_map = {
        'remember that': '',
        'you are': 'i am',
        'i am': 'you are',
        'you have': 'i have',
        'i have': 'you have',
        'you were': 'i was',
        'i was': 'you were',
        'you had': 'i had',
        'i had': 'you had',
        'my':'your',
        'your':'my',
        'we are' : 'you are',
        'we have' : 'you have',
        'we were' : 'you were',
        'we had' : 'you had',
        'myself':'yourself',
        'yourself':'myself',
        'myself':'yourself',        

    }
    
    # Create regex pattern to match whole words case-insensitively
    pattern = re.compile(
        r'\b(' + '|'.join(map(re.escape, replacement_map.keys())) + r')\b',
        flags=re.IGNORECASE
    )
    
    # Replace matched phrases
    def replacer(match):
        key = match.group(1).lower()
        return replacement_map[key]
    
    processed_line = pattern.sub(replacer, new_line)
    
    # Check for existing lines and write
    try:
        with open(file_path, 'r') as file:
            existing_lines = {line.strip() for line in file}
    except FileNotFoundError:
        existing_lines = set()
    
    if processed_line.strip() not in existing_lines:
        with open(file_path, 'a') as file:
            file.write(processed_line.strip() + '\n')
            return f"You told me to remember that: {processed_line.strip()}"
    else:
        return "The line already exists in the memory."